class man:
    def __init__(self,pref=[],num):
        self.prefer=pref
        self.spouse=-1
        self.cur=-1
        self.num=num

    def setpref(self,pref):
        self.prefer=pref

    def propose(self,W):
        self.cur=self.cur+1
        ac=W[self.prefer[self.cur]].response(self.num)
        if ac:
            self.spouse=self.cur

    def inform_break(self):
        self.spouse=-1


class woman:
    def __init__(self,pref=[],num):
        self.matched=False
        self.num=num
        if len(pref)>0:
            self.setscore(pref)
        else:
            self.score=[]

    def setscore(self,pref):
        n=len(pref)
        self.score=[0 for i in range(n)]
        for i in range(n):
            self.score[pref(i)]=n-i

    def response(self,m):
        if !self.matched:
            self.matched=True
            self.spouse=m
            return True
        else:
            if self.score[m.num]>self.score[self.spouse.num]:
                self.spouse.inform_break()
                self.spouse=m
                return True
            else:
                return False

class matcher:
    def __init__(self,filename):
        self.W=[]
        self.M=[]
        fhand=open(filename)
        for line in fhand:
            info=line.split()
            if info[1]='m':
