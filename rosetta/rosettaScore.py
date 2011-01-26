def get_table(path):
    raw_table = []
    infile = open(path,'r')
    table = False
    for line in infile:
        line_split = line.split()
        if len(line_split) <1:
            break
        if line_split[0] == "#BEGIN_POSE_ENERGIES_TABLE":
            table =True
            raw_table.append(line)
        #elif table and line_split[0] == "#END_POSE_ENERGIES_TABLE":
        #    raw_table.append(line)
        #    break
        elif table:
            raw_table.append(line)
    infile.close()
    return raw_table

class ScoreRecord:
    def __init__(self,name,resid,scores):
        self.name = name
        self.resid = resid
        self.scores = scores

class PoseScoreRecord:
    def __init__(self,tag):
        self.tag = tag
        self.score = {}
    def add_score(self,name,value):
        self.score[name] = value

    def get_score(self,name):
        return self.score[name]
    
    def get_tag(self):
        return self.tag

def score_pairs(list):
    for i in xrange(0,len(list),2):
        yield(list[i],float(list[i+1]))


class SilentScoreTable:
    def __init__(self):

        self.records = {}

    def add_file(self,path,ignore_ref=True):
        infile = open(path,'r')
        for line in infile:
            if len(line)== 0:
                continue
            line = line.split()
            if line[0] == "SCORES": #this is an atom tree diff file
                tag = line[1]
                if ignore_ref and tag[0:5] =="%REF%":
                    continue
                    
                record = PoseScoreRecord(tag)
                
                scorefields = line[2:len(line)]
                try:
                    for pair in score_pairs(scorefields):
                        record.add_score(*pair)
                    self.records[tag] = record
                except ValueError:
                    print "theres some problem with this score line, possible corruption, skipping line"
                    continue
                #elif line[0] == "SCORE:" #this is normal silent file
            
        infile.close()
        
    def tag_exists(self,tag):
        return tag in self.records

    def get_score(self,tag,scoreterm):
        try:
            return self.records[tag].get_score(scoreterm)
        except KeyError:
            print "no",scoreterm,"in",tag,"returning 0"
            return 0

    def score_generator(self,scoreterm):
        for tag in self.records.keys():
            try:
                yield self.records[tag].get_score(scoreterm)
            except KeyError:
                print "no",scoreterm,"in",tag,"returning 0"
                yield 0
        
                
        
class ScoreTable:
    def __init__(self,path):
        infile = open(path,'r')
        table = False
        header=[]
        self.weights = {}
        self.records = {}
        for line in infile:
            if len(line) == 0:
                continue
            line = line.split()
            if line[0] == "#BEGIN_POSE_ENERGIES_TABLE":
                table =True
            elif line[0] == "#END_POSE_ENERGIES_TABLE":
                break
            elif table and line[0] == "label":
                header = line[1:len(line)]
            elif table and line[0] =="weights":
                weightline = line[1:len(line)]
                for term, weight in zip(header,weightline):
                    if(weight != "NA"):
                        weight = float(weight)
                        self.weights[term] = weight
                    else:
                        self.weights[term] = 1.0
            elif table:
                name = line[0]
                if name != "pose":
                    resid = int(name.split("_").pop())
                else:
                    resid = 0
                scores = line[1:len(line)]
                scoredict = {}
                for term, score in zip(header,scores):
                    score = float(score)
                    scoredict[term] = score
                self.records[resid] = ScoreRecord(name,resid,scoredict)
        infile.close()
    def get_score(self,resid,term):
        score_record = self.records[resid]
        return score_record.scores[term]

    def get_weight(self,term):
        return self.weights[term]
