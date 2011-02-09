class RosettaLoop:
    def __init__(self):
        self.start = 0
        self.end = 0
        self.cutpoint = 0
        self.skip = 0.0
        self.extend = False
        
    def set_loop(self,start,end,cutpoint,skip,extend):
        self.start = start
        self.end = end
        self.cutpoint = cutpoint
        self.skip = skip
        self.extend = extend
        
    def set_loop_from_string(self,loopstring):
        loop_array = loopstring.split()
        self.start = int(loop_array[1])
        self.end = int(loop_array[2])
        self.cutpoint = int(loop_array[3])
        self.skip = float(loop_array[4])
        if loop_array[4] =="0":  #this is the way it works in C++, we'll mimic it here for compatability
            self.extend = False
        else:
            self.extend = True
    
    def to_string(self):
        if self.extend:
            return "LOOP "+str(self.start)+" "+str(self.end)+" "+str(self.cutpoint)+" "+str(self.skip)+" "+str(1)
        else:
            return "LOOP "+str(self.start)+" "+str(self.end)+" "+str(self.cutpoint)+" "+str(self.skip)+" "+str(0)

class RosettaLoopManager:
    def __init__(self):
        self.looplist = []
    
    def __iter__(self):
        return iter(self.looplist)
        
    def read(self,filename,append=False):
        if not append:
            self.looplist = []
        loop_file = open(filename,"rU")
        for line in loop_file:
            loop = RosettaLoop()
            loop.set_loop_from_string(line)
            self.looplist.append(loop)
        loop_file.close()
    
    def write(self,filename):
        loop_file = open(filename,"w")
        for loop in self.looplist:
            loop_file.write(loop.to_string()+"\n")
        loop_file.close()
        
    def is_res_in_loop(self,resnum):
        for loop in self.looplist:
            if loop.start <= resnum and loop.end >= resnum:
                return True
        return False
        
    def add_loop(self,start,end,cutpoint,skip,extend):
        loop = RosettaLoop()
        loop.set_loop(start,end,cutpoint,skip,extend)
        self.looplist.append(loop)
    
    