import execflags
from itertools import cycle
from instruction import *
import common
import indexing

class listpop_t(indexing.getat_t):
    """
    This is just syntactic sugar for -1].
    """
    def execute(self,stack,exec_env):
        if len(stack) < 1:
            instr_t.execute(self,stack,exec_env)
            return
        stack=common.stack_push(stack,-1)
        indexing.getat_t.execute(self,stack,exec_env)

def listpop_instr_contr(matches,parser):
    return listpop_t()

def listpush(l,r,outer):
    tc=''.join(map(common.typecode,[l,r]))
    return getattr(_listpush_vtable,tc)(l,r,outer)

class _listpush_vtable:
    def nn(l,r,outer):
        return [l,r]
    def ln(l,r,outer):
        return l + [r]
    def Ln(l,r,outer):
        if outer:
            return [ listpush(x,r,outer) for x in l ]
        return l + [r]
    def nl(l,r,outer):
        return [l] + r
    def ll(l,r,outer):
        if outer:
            for x in r:
                l.append(x)
            return l
        return l + [r]
    def Ll(l,r,outer):
        if outer:
            return [ listpush(x,y,outer) for x,y in zip(l,cycle(r)) ]
        return l + [r]
    def nL(l,r,outer):
        if outer:
            return [ listpush(l,x,outer) for x in r ]
        return [l] + r
    def lL(l,r,outer):
        if outer:
            return [ listpush(x,y,outer) for x,y in zip(l,cycle(r)) ]
        return l + [r]
    def LL(l,r,outer):
        if outer:
            return [ listpush(x,y,outer) for x,y in zip(l,cycle(r)) ]
        return l + [r]

class listpush_t(instr_t):
    def execute(self,stack,exec_env):
        """
        Appends last item on stack to item before if it is a list,
        if the stack only contains 1 item, make this item into a list
        if the penultimate stack item isn't a list, make it so before appending the
        item
        """
        if len(stack) < 1:
            instr_t.execute(self,stack,exec_env)
            return
        x=stack.pop()
        if len(stack) == 0:
            stack=common.stack_push(stack,[x])
            instr_t.execute(self,stack,exec_env)
            return
        y=stack.pop()
        outer=(execflags.OUTEROP in exec_env.flgs)
        y=listpush(y,x,outer)
        stack=common.stack_push(stack,y)
        instr_t.execute(self,stack,exec_env)

def listpush_instr_contr(matches,parser):
    return listpush_t()

