import sys
import PSSM
from Bio.PDB import * 
import math


def load_pdb(path):
	parser = PDBParser(PERMISSIVE=1)
	structure = parser.get_structure(path[0:4],path)
	return structure

def sequence_recovery(native_struct,designed_struct):
	
	native_residues = native_struct.get_residues()
	designed_residues = designed_struct.get_residues()
	total = 0.0;
	recovered = 0.0;
	for native,designed in zip(native_residues,designed_residues):
		if native.get_resname() == designed.get_resname():
			recovered += 1
		total += 1
	#print recovered, total
	return recovered/total

def sequence_recovery_range(native_struct,designed_struct,min,max):
	native_residues = native_struct.get_residues()
	designed_residues = designed_struct.get_residues()
	total = 0.0
	recovered = 0.0
	for native,designed in zip(native_residues,designed_residues):
		score = native.get_list()[1].get_bfactor()
		if score >= min and score <= max:
			if native.get_resname() == designed.get_resname():
				recovered += 1
			total += 1
	return recovered/total

def sequence_recovery_group(native_struct,designed_struct,min,max):
	non_polar = ["GLY","ALA","VAL","LEU","MET","ILE"]
	polar = ["SER","THR","CYS","PRO","ASN","GLN"]
	aromatic = ["PHE","TYR","TRP"]
	charged = ["LYS","ARG","HIS","ASP","GLU"]

	groups = {"non_polar":non_polar,"polar":polar,"aromatic":aromatic,"charged":charged}
	

	native_residues = native_struct.get_residues()
	designed_residues = designed_struct.get_residues()
	total = {"non_polar" :0.0, "polar":0.0, "aromatic":0.0, "charged":0.0}
	recovered = {"non_polar" :0.0, "polar":0.0, "aromatic":0.0, "charged":0.0}

	for native,designed in zip(native_residues,designed_residues):
		score = native.get_list()[1].get_bfactor()
		
		if score >= min and score <= max:
			for group in groups:
				if native.get_resname() in groups[group] and designed.get_resname() in groups[group]:
					recovered[group] += 1
				if designed.get_resname() in groups[group]:
					total[group] += 1
					break
	for group in groups:
		print group,recovered[group],total[group]
		#recovered[group]=recovered[group]/total[group]

	return recovered

	

def sequence_composition(struct):
	struct_residues = struct.get_residues()
	composition = {}
	for residue in struct_residues:
		residue_name = residue.get_resname()
		try:
			composition[residue_name]+=1
		except KeyError:
			composition[residue_name] = 1 
	return composition
	
def sequence_composition_range(struct,min,max):
	struct_residues = struct.get_residues()
	composition = {}
	for residue in struct_residues:
		score = residue.get_list()[1].get_bfactor()
		if score >= min and score <= max:
			residue_name = residue.get_resname()
			try:
				composition[residue_name]+=1
			except KeyError:
				composition[residue_name] = 1 
	return composition

def pssm_recovery_map(struct,pssm_map):
	struct_residues = struct.get_residues()
	#pssm_recovery = 0.0;
	#struct_size = 0.0;
	recovery_map = {}
	for residue in struct_residues:
		residue_name = residue.get_resname()
		residue_num = residue.get_id()[1]
		status = pssm_map.conserved(residue_num,residue_name)
		if status:
			try:
				recovery_map[residue_name]+=1
			except KeyError:
				recovery_map[residue_name] = 1
	return recovery_map

def pssm_recovery_map_range(struct,pssm_map,min,max):
	struct_residues = struct.get_residues()
	recovery_map = {}
	for residue in struct_residues:
		score = residue.get_list()[1].get_bfactor()
		if score >= min and score <= max:
			residue_name = residue.get_resname()
			residue_num = residue.get_id()[1]
			status = pssm_map.conserved(residue_num, residue_name)
			if status:
				try:
					recovery_map[residue_name]+= 1
				except KeyError:
					recovery_map[residue_name] = 1
	return recovery_map

def pssm_recovery(struct,pssm_map):
	struct_residues = struct.get_residues()
	pssm_recovery = 0.0;
	struct_size = 0.0;
	for residue in struct_residues:
		residue_name = residue.get_resname()
		residue_num = residue.get_id()[1]
		status = pssm_map.conserved(residue_num,residue_name)
		if status:
			pssm_recovery += 1.0
		struct_size += 1.0
	return pssm_recovery/struct_size

def pssm_recovery_range(struct,pssm_map,min,max):
	pssm_recovery = 0.0;
	struct_size = 0.0;
	for residue in struct.get_residues():
		score= residue.get_list()[1].get_bfactor()
		#print score
		if score >= min and score <= max:
			residue_name = residue.get_resname()
			residue_num = residue.get_id()[1]
			status = pssm_map.conserved(residue_num,residue_name)
			if status:
				pssm_recovery += 1.0
			struct_size += 1.0
			
	return pssm_recovery/struct_size

def pssm_scores(struct,pssm_map):
	struct_residues = struct.get_residues()
	pssm_scores = {}
	size = 0
	for residue in struct_residues:
		size += 1
		residue_name = residue.get_resname()
		residue_num = residue.get_id()[1]
		try:
			pssm_scores[residue_name] += pssm_map.get_score(residue_num,residue_name)
		except KeyError:
			pssm_scores[residue_name] = pssm_map.get_score(residue_num,residue_name)
	for key in pssm_scores:
		pssm_scores[key] = pssm_scores[key]/size
	return pssm_scores


def pssm_scores_range(struct,pssm_map,min,max):
	struct_residues = struct.get_residues()
	pssm_scores = {}
	size = 0
	for residue in struct_residues:
		score = residue.get_list()[1].get_bfactor()
		#print score
		if score >= min and score <= max:
			size += 1
			residue_name = residue.get_resname()
			residue_num = residue.get_id()[1]
			try:
				pssm_scores[residue_name] += pssm_map.get_score(residue_num,residue_name)
			except KeyError:
				pssm_scores[residue_name] = pssm_map.get_score(residue_num,residue_name)
	for key in pssm_scores:
		pssm_scores[key] = pssm_scores[key]/size
	return pssm_scores


def ca_rms_only(struct_a,struct_b,residue_list):
	residues_a = struct_a.get_residues();
	residues_b = struct_b.get_residues();

	d_2_sum = 0.0
	resn = 0
	for (res_a, res_b) in zip(residues_a, residues_b):
		if res_a.get_id()[1] not in residue_list:
			continue
		CA_a = res_a['CA']
		CA_b = res_b['CA']

		distance_2 = (CA_a-CA_b)**2
		d_2_sum += distance_2
		resn += 1
		
	rmsd = math.sqrt(d_2_sum/resn)
	return rmsd


def atom_rms(atoms_a,atoms_b,residue_list):

	d_2_sum = 0.0
	resn = 0
	for(atom_a,atom_b) in zip(atoms_a,atoms_b):
		parent_a = atom_a.get_parent()
		if parent_a.get_id()[1] in residue_list:
			#print "calculating for",parent_a.get_id()[1]
			distance_2 = (atom_a-atom_b)**2
			d_2_sum += distance_2
			resn +=1
		else:
			continue
			


	
	rmsd = math.sqrt(d_2_sum/resn)
	return rmsd	

def copy_b_factor(native_pdb,designed_pdb):
	native_atoms = native_pdb.get_atoms()
	designed_atoms = designed_pdb.get_atoms()
	for native_atom, designed_atom in zip(native_atoms, designed_atoms):
		designed_atom.set_bfactor(native_atom.get_bfactor)
	return designed_pdb

