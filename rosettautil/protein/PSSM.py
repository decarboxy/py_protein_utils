import Bio.PDB.Polypeptide
from rosettautil.util import fileutil

class pssm_map:
	def __init__(self,path):
		"""Parse a PSSM file from BLAST into a usable datastructure"""
		self.pssmmap = {}
		pssmfile = fileutil.universal_open(path,'r')

		
		pssmfile.readline()
		pssmfile.readline()
	
		header = pssmfile.readline()
		header = header.split()
		header = header[0:21]
		for line in pssmfile:
			#print line
			line = line.split()

			if len(line) == 0:
				break
		
			res_num = int(line[0])
			res_id = line[1]
		
			line_map = {}
			for resname,score in zip(header,line[2:23]):
				line_map[resname] = int(score)
			self.pssmmap[res_num] = line_map

		pssmfile.close()
	
	def get_score(self,seqpos,resname):
		"""get the score for a given sequence position and residue name"""
		if len(resname) == 3:
			resname =  Bio.PDB.Polypeptide.three_to_one(resname)
			linemap = self.pssmmap[seqpos]
			return linemap[resname]
			
		elif len(resname) == 1:
			linemap = self.pssmmap[seqpos]
			return linemap[resname]
		else:
			raise LookupError("this isn't a residue")

	def conserved(self,seqpos,resname):
		"""return true if the score of a given sequence position and residue name is greater than 0"""
		score = self.get_score(seqpos,resname)
		if(score >=0):
			return True
		else:
			return False
