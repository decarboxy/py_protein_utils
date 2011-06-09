import Bio.PDB.Polypeptide
from rosettautil.util import fileutil

class sasa_point:
    def __init__(self,resname, chain,resnum, type,absolute,relative):
        self.resname = resname
        self.resnum = resnum
        self.chain = chain
        self.type = type
        self.absolute = absolute
        self.relative = relative
        
class sasa_map:
    def __init__(self):
        self.all = {}
        self.sidechain = {}
        self.mainchain = {}
        self.nonpolar = {}
        self.polar = {}
    
    def add_item(self,resname, chain,resnum,type,absolute,relative):
        new_point = sasa_point(resname,chain,resnum,type,absolute,relative)
        if type == "all":
            self.all[ (resnum,chain) ] = new_point
        elif type == "sidechain":
            self.sidechain[ (resnum,chain) ] = new_point
        elif type == "mainchain":
            self.mainchain[ (resnum, chain) ] = new_point
        elif type == "nonpolar":
            self.nonpolar[ (resnum, chain) ] = new_point
        elif type == "polar":
            self.polar[ (resnum, chain) ] = new_point
    
    def get_value(self,chain,resnum,type,mode):
        if type == "all":
            point = self.all[ (resnum,chain) ] 
        elif type == "sidechain":
            point = self.sidechain[ (resnum,chain) ]
        elif type == "mainchain":
            point = self.mainchain[ (resnum,chain) ]
        elif type == "nonpolar":
            point = self.nonpolar[ (resnum,chain) ]
        elif type == "polar":
            point = self.polar[ (resnum,chain) ]
        
        if mode == "absolute":
            return point.absolute
        elif mode == "relative":
            return point.relative

class sasa_map:
    def __init__(self,path):
        
        self.sasamap = sasa_map()
        sasafile = fileutil.universal_open(path,'r')
        __parse__(sasafile)
        sasafile.close()
        
    def __parse__(self,file):
        for line in file:
            line = line.split()
            if line[0] != "RES":
                continue
            
            resname = line[1]
            chain = line[2]
            resnum = int(line[3])
            
            all_abs = float(line[4])
            all_rel = float(line[5])
            self.sasamap.add_item(resname,chain,resnum,"all", all_abs,all_rel)
            
            side_abs = float(line[6])
            side_rel = float(line[7])
            self.sasamap.add_item(resname,chain,resnum,"all", all_abs,all_rel)
            
            main_abs = float(line[8])
            main_rel = float(line[9])
            
            apol_abs = float(line[10])
            apol_rel = float(line[11])
            
            pol_abs = float(line[12])
            pol_rel = float(line[13])
            

            
            