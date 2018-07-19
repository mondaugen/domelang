import execflags
import common
from instruction import *
from itertools import cycle

__doc__="""
Operators for getting and setting elements of lists.
"""

class _vindex_set_vtable:
    def nnn(l,m,r):
        return r
    def nnl(l,m,r):
        if len(r) == 0:
            return None
        return r[int(round(0))]
    def nln(l,m,r):
        return r
    def nll(l,m,r):
        if len(r) == 0:
            return None
        return r[-1]
    def nlL(l,m,r):
        return l
    def nLn(l,m,r):
        return r
    def nLl(l,m,r):
        return l
    def nLL(l,m,r):
        return l
    def lnn(l,m,r):
        if len(l) == 0:
            return None
        l[int(round(m))%len(l)]=r
        return l
    def lnl(l,m,r):
        if len(l) == 0:
            return None
        l[int(round(m))%len(l)]=r
        return l
    def lnL(l,m,r):
        if len(l) == 0:
            return None
        l[int(round(m))%len(l)]=r
        return l
    def lln(l,m,r):
        if len(l) == 0:
            return None
        for i in m:
            l[int(round(i))%len(l)]=r
        return l
    def lll(l,m,r):
        if len(l) == 0:
            return None
        for a,b in zip(m,cycle(r)):
            l[int(round(a))%len(l)]=b
        return l
    def llL(l,m,r):
        if len(l) == 0:
            return None
        for a,b in zip(m,cycle(r)):
            l[int(round(a))%len(l)]=b
        return l
    def lLn(l,m,r):
        for a in m:
            l=vindex_set(l,a,r)
        return l
    def lLl(l,m,r):
        for a in m:
            l=vindex_set(l,a,r)
        return l
    def lLL(l,m,r):
        for a,b in zip(m,cycle(r)):
            l=vindex_set(l,a,b)
        return l
    def Lnn(l,m,r):
        if len(l) == 0:
            return None
        for i,a in enumerate(l):
            l[int(round(i))%len(l)]=vindex_set(a,m,r)
        return l
    def Lnl(l,m,r):
        if len(l) == 0:
            return None
        l[int(round(m))%len(l)]=r
        return l
    def LnL(l,m,r):
        if len(l) == 0:
            return None
        l[int(round(m))%len(l)]=r
        return l
    def Lln(l,m,r):
        if len(l) == 0:
            return None
        for i,a in enumerate(l):
            l[int(round(i))%len(l)]=vindex_set(a,m,r)
        return l
    def Lll(l,m,r):
        if len(l) == 0:
            return None
        for i,a in enumerate(l):
            l[int(round(i))%len(l)]=vindex_set(a,m,r)
        return l
    def LlL(l,m,r):
        if len(l) == 0:
            return None
        for i,(a,b) in enumerate(zip(l,cycle(r))):
            l[int(round(i))%len(l)]=vindex_set(a,m,b)
        return l
    def LLn(l,m,r):
        if len(l) == 0:
            return None
        for i,(a,b) in enumerate(zip(l,cycle(m))):
            l[int(round(i))%len(l)]=vindex_set(a,b,r)
        return l
    def LLl(l,m,r):
        if len(l) == 0:
            return None
        for i,(a,b) in enumerate(zip(l,cycle(m))):
            l[int(round(i))%len(l)]=vindex_set(a,b,r)
        return l
    def LLL(l,m,r):
        if len(l) == 0:
            return None
        for i,(a,b,c) in enumerate(zip(l,cycle(m),cycle(r))):
            l[int(round(i))%len(l)]=vindex_set(a,b,c)
        return l

def vindex_set(l,m,r):
    tc=''.join(map(common.typecode,[l,m,r]))
    return getattr(_vindex_set_vtable,tc)(l,m,r)

class setat_t(instr_t):
    name = 'SETAT'
    def execute(self,stack,exec_env):
        if len(stack) >= 3:
            r=stack.pop()
            m=stack.pop()
            l=stack.pop()
            stack=common.stack_push(stack,vindex_set(l,m,r))
        instr_t.execute(self,stack,exec_env)

def setat_instr_constr(matches,parser):
    return setat_t()

class _vindex_get_vtable:
    def nn(l,r,outer):
        return l
    def ln(l,r,outer):
        if len(l) == 0:
            return None
        return l[int(round(r))%len(l)]
    def nl(l,r,outer):
        if len(r) == 0:
            return None
        return [l for _ in r]
    def nL(l,r,outer):
        if len(r) == 0:
            return None
        return [vindex_get(l,x,outer) for x in r]
    def Ln(l,r,outer):
        if outer:
            return [vindex_get(x,r,outer) for x in l]
        if len(l) == 0:
            return None
        return l[int(round(r))%len(l)]
    def ll(l,r,outer):
        return [l[int(round(x))%len(l)] for x in r]
    def lL(l,r,outer):
        return [vindex_get(l,x,outer) for x in r]
    def Ll(l,r,outer):
        if outer:
            return [vindex_get(x,r,outer) for x in l]
        if len(l) == 0:
            return None
        return [l[int(round(x))%len(l)] for x in r]
    def LL(l,r,outer):
        if outer:
            return [vindex_get(l,x,outer) for x in r]
        return [vindex_get(x,y,outer) for x,y in zip(l,cycle(r))]

def vindex_get(l,r,outer):
    tc=''.join(map(common.typecode,[l,r]))
    return getattr(_vindex_get_vtable,tc)(l,r,outer)

class getat_t(instr_t):
    name = 'GETAT'
    def execute(self,stack,exec_env):
        if len(stack) >= 2:
            r=stack.pop()
            l=stack.pop()
            outer=(execflags.OUTEROP in exec_env.flgs)
            stack=common.stack_push(stack,vindex_get(l,r,outer))
        instr_t.execute(self,stack,exec_env)

def getat_instr_constr(matches,parser):
    return getat_t()
