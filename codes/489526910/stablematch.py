class man:
    def __init__(self,num,pref=[]):
        self.prefer=pref
        self.spouse=-1
        self.id=num

    def setpref(self,pref):
        self.prefer=pref

    def propose(self,W):
        target=self.prefer.pop(0)
        re,ex=W[target-1].response(self)
        if re:
            self.spouse=target
        return re,ex


    def inform_break(self):
        self.spouse=-1


class woman:
    def __init__(self,num,pref=[]):
        self.matched=False
        self.id=num
        if len(pref)>0:
            self.setscore(pref)
        else:
            self.score=[]

    def setscore(self,pref):
        n=len(pref)
        self.score=[0 for i in range(n)]
        for i in range(n):
            self.score[pref[i]-1]=n-i

    def response(self,m):
        if not self.matched:
            self.matched=True
            self.spouse=m
            return True,-1
        else:
            if self.score[m.id-1]>self.score[self.spouse.id-1]:
                ex=self.spouse.id
                self.spouse=m
                return True,ex
            else:
                return False,-1


class matcher:
    def __init__(self,man_file,woman_file):
        self.W=[]
        self.M=[]
        self.single_man=[]
        fhandm=open(man_file)
        for line in fhandm:
            info=line.split()
            self.M.append(man(num=int(info[0]),pref=map(int,info[1:])))
            self.single_man.append(int(info[0])-1)
        fhandm.close()

        fhandw=open(woman_file)
        for line in fhandw:
            info=line.split()
            self.W.append(woman(num=int(info[0]),pref=map(int,info[1:])))

    def stable_match(self):
        while True:
            i=self.single_man.pop()
            re,ex=self.M[i].propose(self.W)
            if re:
                if ex>0:
                    self.M[ex-1].inform_break()
                    self.single_man.append(ex-1)
            else:
                self.single_man.append(i)
            if len(self.single_man)==0:
                break

    def declaim(self):
        self.marriage=[]
        for i in self.M:
            self.marriage.append((i.id,i.spouse))
        for i in self.marriage:
            print i



ma=matcher('test1_man.txt','test1_woman.txt')
ma.stable_match()
ma.declaim()
