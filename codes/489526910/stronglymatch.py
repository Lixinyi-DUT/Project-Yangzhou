from hopcroftkarp import HopcroftKarp

class man:
    def __init__(self,num,pref,n):
        self.pref=[0 for i in range(n)]
        self.leader=list(self.pref)
        self.spouse=[]
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
        head=self.pref.index(self.leader[0])
        losers=[]
        ex=[]
        w=[]
        for target in self.pref[:head+1]:
            losers_m,ex_m=W[target-1].response(self)
            losers.append(losers_m)
            ex.append(ex_m)
            w.append(target)
            self.spouse.append(target)
        self.pref=list(self.pref[head+1:])
        self.leader=list(self.leader[head+1:])
        return losers,ex,w


    def inform_break(self,w):
        if w in self.spouse:
            self.spouse.remove(w)
        if len(self.spouse)>0:
            return False
        else:
            return True


    def inform_fail(self,w):
        if w in self.pref:
            p=self.pref.index(w)
            self.leader.pop(p)
            self.pref.pop(p)


class woman:
    def __init__(self,num,pref,n):
        self.id=num
        self.spouse=[]
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
        pos=self.pref.index(m.id)
        eq=self.leader[pos]
        last=self.pref.index(eq)
        ex=[]
        if len(self.spouse)>0:
            cur=self.spouse[0]
            pos_cur=self.pref.index(cur.id)
            eq_cur=self.leader[pos_cur]
            if not eq_cur==eq:
                ex=[x.id for x in self.spouse]
                self.spouse=[]

        self.spouse.append(m)
        losers=self.pref[last+1:]
        self.pref=self.pref[:last+1]
        self.leader=self.leader[:last+1]

        return losers,ex

    def break_all_relationship(self):
        if len(self.spouse)>0:
            tail=self.leader.index(self.pref[-1])
            ex=[m.id for m in self.spouse]
            self.spouse=[]
            losers=self.pref[tail:]
            self.pref=self.pref[:tail]
            self.leader=self.leader[:tail]
            return True,ex,losers
        else:
            return True,[],[]

class matcher:
    def __init__(self,man_file,woman_file):
        self.M=[]
        self.W=[]
        self.single_man=[]
        M_id,M_pref=self.read_prefmatrix(man_file)
        self.n=len(M_id)
        for i in range(self.n):
            self.M.append(man(M_id[i],M_pref[i],self.n))
            self.single_man.append(i+1)
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

    def critical_set(self):
        graph=dict()
        U=[] # unmatched men in maximum cardinality matching
        R=[] # men that can be reached from men in U via alternating paths
        c_set=[]
        for m in self.M:
             graph[m.id+self.n]=m.spouse
        max_matching=HopcroftKarp(graph).maximum_matching()
        for i in range(self.n):
            if i+11 not in max_matching:
                U.append(i)
        for i in range(self.n):
            if i+1 in max_matching:
                for j in self.W[i].spouse:
                    if j.id != max_matching[i+1]:
                        R.append(j.id-1)
        return U+R,max_matching


    def stable_match(self):
        a=0
        while True:
            while len(self.single_man)>0:
                i=self.single_man.pop()
                if len(self.M[i-1].pref)==0:
                    return False
                losers,ex,w=self.M[i-1].propose(self.W)
                for j in range(len(w)):
                    for ex_m in ex[j]:
                        if self.M[ex_m-1].inform_break(w[j]):
                            self.single_man.append(ex_m)
                    for m in losers[j]:
                        self.M[m-1].inform_fail(w[j])

            cri_set,matching=self.critical_set()
            if len(cri_set)==0:
                for v in max_matching:
                    if v>self.n:
                        M[v-self.n-1].spouse=[max_matching[v]]
                    else:
                        W[v-1].spouse=[M[max_matching[v]-self.n]]
            return True

            for m in cri_set:
                for w in self.M[m-1].spouse:
                    br,ex,losers=w.break_all_relationship()
                    if br:
                        for ex_m in ex:
                            if self.M[ex_m-1].inform_break(w.id):
                                self.single_man.append(m)
                        for loser_m in losers:
                            self.M[loser_m-1].inform_fail(w.id)


    def declaim(self):
        self.marriage=[]
        for i in self.M:
            self.marriage.append((i.id,i.spouse[0]))
        for i in self.marriage:
            print i



ma=matcher('test2_man.txt','test2_woman.txt')
if ma.stable_match():
    ma.declaim()
else:
    print False
