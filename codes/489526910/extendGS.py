class man:
    def __init__(self,num,pref,n):
        self.pref=[0 for i in range(n)]
        self.leader=list(self.pref)
        self.spouse=-1
        self.id=num
        self.setpref(pref)

    def setpref(self,l):
        i=0
        for item in l:
            if type(item) is list:
                for j in item:
                    self.pref[i]=j
                    self.leader[i]=item[-1]
                    i=i+1
            else:
                self.pref[i]=item
                self.leader[i]=item
                i=i+1

    def propose(self,W):
        target=self.pref.pop(0)
        self.leader.pop(0)
        losers,ex=W[target-1].response(self)
        self.spouse=target
        return losers,ex,target


    def inform_break(self):
        self.spouse=-1

    def inform_fail(self,w):
        if w in self.pref:
            p=self.pref.index(w)
            self.leader.pop(p)
            self.pref.pop(p)

class woman:
    def __init__(self,num,pref,n):
        self.matched=False
        self.id=num
        self.pref=[0 for i in range(n)] #Initialize
        self.leader=list(self.pref) #leader is a vector to record equivalence
        self.setpref(pref)

    def setpref(self,l):
        i=0
        for item in l:
            if type(item) is list:
                for j in item:
                    self.pref[i]=j
                    self.leader[i]=item[-1]
                    i=i+1
            else:
                self.pref[i]=item
                self.leader[i]=item
                i=i+1

    def response(self,m):
        ex=-1
        if self.matched:
            ex=self.spouse.id
        else:
            self.matched=True
        self.spouse=m

        pos=self.pref.index(m.id)
        eq=self.leader[pos]
        last=self.pref.index(eq)
        losers=self.pref[last+1:]

        return losers,ex

class matcher:
    def __init__(self,man_file,woman_file):
        self.M=[]
        self.W=[]
        self.single_man=[]
        M_id,M_pref=self.read_prefmatrix(man_file)
        self.n=len(M_id)
        for i in range(self.n):
            self.M.append(man(M_id[i],M_pref[i],self.n))
            self.single_man.append(i)
        W_id,W_pref=self.read_prefmatrix(woman_file)
        for i in range(self.n):
            self.W.append(woman(W_id[i],W_pref[i],self.n))

    def read_prefmatrix(self,fname):
        result=[]
        numbers=[]
        fhand=open(fname)
        for line in fhand:
            pref_v=[] # pref_v[0]: number of the info
            temp=[]
            info=line.split()
            for i in info:
                if i =='[':
                    pref_v=pref_v+temp
                    temp=[]
                elif i == ']':
                    pref_v.append(temp)
                    temp=[]
                else:
                    temp.append(int(i))
            pref_v=pref_v+temp
            numbers.append(pref_v.pop(0))
            result.append(pref_v)
        fhand.close()
        return numbers,result


    def stable_match(self):
        while True:
            i=self.single_man.pop()
            losers,ex,w=self.M[i].propose(self.W)
            if ex>0:
                self.M[ex-1].inform_break()
                self.single_man.append(ex-1)
            for m in losers:
                self.M[m-1].inform_fail(w)
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
