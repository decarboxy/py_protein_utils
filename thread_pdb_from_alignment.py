#!/usr/bin/python
from Bio import AlignIO
import Bio.PDB
from optparse import OptionParser
import sys
import array
from protein import pdbStat
from protein import alignment



usage = "%prog [options] alignment_file.aln template.pdb output.pdb"
parser=OptionParser(usage)
parser.add_option("--template",dest="template",help="name of the template sequence", Default="template")
parser.add_option("--alignment", dest ="alignment",help="name of the alignment sequence",Default="alignment")
parser.add_option("--chain",dest="chain",help="chain to thread pdb around")
parser.add_option("--align_format",dest="align_format",help="alignment file format, choose from clustal, emboss, fasta, fasta-m10,ig,nexus,phylip,stockholm.  See http://biopython.org/wiki/AlignIO for details"Default="clustal")
(options,args)= parser.parse_args()

#read in our input files
alignment = AlignIO.read(args[0],options.align_format)
template_struct = pdbStat.load_pdb(args[1])

if len(alignment)  != 2:
    sys.exit("alignment file must have exactly 2 sequences!") 

#find all the gaps, get numeric IDs from the string tags in the alignment file
template_gaps = alignment.find_gaps(alignment,options.template)
alignment_gaps = alignment.find_gaps(alignment,options.alignment)
template_id = alignment.get_id_from_tag(alignment,options.template)
alignment_id = alignment.get_id_from_tag(alignment,options.alignment)

#if you have an alignment gap thats larger than 3 aa, this script won't work
for gap in alignment_gaps:
    if gap[0]-gap[1] > 3:
        sys.exit("gap of size "+ str(gap[0]-gap[1])+" in alignment sequence.  You cannot have gaps larger than 3 in your alignment sequence")

#we need to make a new structure, then a new model, then a new chain, then we fill the chain with residues, and atoms
output_structure_builder = Bio.PDB.StructureBuilder()
output_structure_builder.init_structure(args[2]) 
output_structure_builder.init_model(1,1) #there is only one model
output_structure_builder.init_chain(options.chain) #there is only one chain, same ID as the template

#thats it for the initialization stuff, now we go through add residues, and atoms.  
template_residues = template_struct.get_residues()
sequence_num = 1 #the pdb sequence number
atom_num = 1 #the atom id
for align_resn, temp_resn in zip(alignment[alignment_id],alignment[template_id]):
    if align_resn == '-' and temp_resn == '-':  #this shouldn't happen, but it is safe to ignore
        continue
    elif align_resn != '-' and temp_resn == '-': #gap in the template, not in the alignment, build a loop
        align_name3 = Bio.PDB.Polypeptide.one_to_three(align_resn)
        output_structure_builder.init_residue(align_name3," ",sequence_num,"")
        zero_triplet = array('f',[0.0,0.0,0.0])
        output_structure_builder.init_atom("N",zero_triplet,0.0,1.0," "," N  ", atom_num, "N")
        atom_num += 1
        output_structure_builder.init_atom("CA",zero_triplet,0.0,1.0," "," CA ",atom_num,"C")
        atom_num += 1
        output_structure_builder.init_atom("C",zero_triplet,0.0,1.0," "," C  ",atom_num,"C")
        atom_num += 1
        output_structure_builder.init_atom("O", zero_triplet,0.0,1.0," "," O  ",atom_num,"O")
        atom_num + = 1
        sequence_num += 1
    elif align_resn == '-' and temp_resn != '-': #gap in the alignment, not in the template, skip the residue
        continue
    elif align_resn != '-' and temp_resn != '-': #we're aligned, copy backbone from old pdb to new, if the sidechain is identical, copy that too
        align_name3 = Bio.PDB.Polypeptide.one_to_three(align_resn)
        temp_name3 = Bio.PDB.Polypeptide.one_to_three(temp_resn)
        current_res = template_residues.next() #pull the next residue out of the pdb file 
        if(current_res.get_resname() != temp_name3):  #if the current residue from the pdb isnt the same type as the current from the template, something's broken
            sys.exit("Residue mismatch between alignment and PDB, check that PDB sequence and alignment sequence are identical")
        output_structure_builder.init_residue(align_name3," ",sequence_num,"")
        if(align_name3 == temp_name3): #if we have an exact alignment, copy all the atoms over, including the sidechain
            for atom in current_res:
                coords = atom.get_coord()
                name = atom.get_name()
                fullname = atom.get_fullname()
                output_structure_builder.init_atom(name,coords,0.0,1.0," ",fullname,atom_num,None)
                atom_num += 1
        else: #we don't have an exact alignment, just copy the backbone coordinates
            #by definition, the first 4 atoms that come out of a residue are N, CA, C, O.  How convenient...
            for atom_index in range(4):
                atom = current_res[atom_index]
                coords = atom.get_coord()
                name = atom.get_name()
                fullname = atom.get_fullname()
                output_structure_builder.init_atom(name,coords,0.0,1.0," ",fullname,atom_num,None)
                atom_num += 1
        sequence_num += 1

#now, output the structure
output_struct = output_structure_builder.get_structure()
pdb_io = Bio.PDB.PDBIO()
pdb_io.set_structure(output_struct)
pdb_io.save(args[2])