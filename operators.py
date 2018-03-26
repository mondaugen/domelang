from instruction import *
import common
from itertools import cycle
import execflags

class _binary_operator_vtable:
    """
    A table of ways to apply a binary operator depending on the argument types.
    """
    def cycle_rhs(l,r,op,outer):
        for i,(x,y) in enumerate(zip(l,cycle(r))):
            l[i]=binary_operator(x,y,op,outer)
        return l
    def outer_rhs(l,r,op,outer):
        for i,x in enumerate(l):
            l[i]=[ binary_operator(x,y,op,outer) for y in r ]
        return l
    def nn(l,r,op,outer):
        return op(l,r)
    def nl(l,r,op,outer):
        if len(r) == 0:
            return None
        return [ op(l,x) for x in r ]
    def nL(l,r,op,outer):
        return [ binary_operator(l,x) for x in r ]
    def ln(l,r,op,outer):
        if len(l) == 0:
            return None
        return [ op(x,r) for x in l ]
    def ll(l,r,op,outer):
        if len(l) == 0 or len(r) == 0:
            return None
        if outer:
            return _binary_operator_vtable.outer_rhs(l,r,op,outer)
        return _binary_operator_vtable.cycle_rhs(l,r,op,outer)
    def lL(l,r,op,outer):
        if len(l) == 0:
            return None
        if outer:
            return _binary_operator_vtable.outer_rhs(l,r,op,outer)
        return _binary_operator_vtable.cycle_rhs(l,r,op,outer)
    def Ln(l,r,op,outer):
        return [ binary_operator(x,r) for x in l ]
    def Ll(l,r,op,outer):
        if len(r) == 0:
            return None
        if outer:
            return _binary_operator_vtable.outer_rhs(l,r,op,outer)
        return _binary_operator_vtable.cycle_rhs(l,r,op,outer)
    def LL(l,r,op,outer):
        if outer:
            return _binary_operator_vtable.outer_rhs(l,r,op,outer)
        return _binary_operator_vtable.cycle_rhs(l,r,op,outer)

def _dyad_divide(x,y):
    return x/y

_dyad_table = {
    '+': lambda x,y: x+y,
    '-': lambda x,y: x-y,
    '÷': _dyad_divide,
    '×': lambda x,y: x*y
}

def binary_operator(l,r,op,outer):
    """
    Applies op to l and r depending on their types and sizes.
    op is a function that takes 2 numbers are returns a number.
    l and r are and valid stack item (number, list, list of lists).
    """
    tc=''.join(map(common.typecode,[l,r]))
    return getattr(_binary_operator_vtable,tc)(l,r,op,outer)

class dyad_t(instr_t):
    """
    Class for binary operators. Operator op passed in upon creation.
    """
    def __init__(self,op):
        instr_t.__init__(self)
        self.op = op

    def execute(self,stack,exec_env):
        if len(stack) >= 2:
            r=stack.pop()
            l=stack.pop()
            outer=(execflags.OUTEROP in exec_env.flgs)
            stack=common.stack_push(stack,binary_operator(l,r,self.op,outer))
        instr_t.execute(self,stack,exec_env)

def dyad_instr_constr(matches,parser):
    return dyad_t(_dyad_table[matches[0]])

class outerop_t(instr_t):
    """
    Class flagging outer operator.
    """
    def execute(self,stack,exec_env):
        exec_env.rqst_flgs.append(execflags.OUTEROP)
        instr_t.execute(self,stack,exec_env)

def outerop_instr_constr(matches,parser):
    return outerop_t()

def opmod_t(instr_t):
    """
    Class allowing operator modification.
    """
    def execute(self,stack,exec_env):
        exec_env.rqst_flgs.append(execflags.OPMOD)
        instr_t.execute(self,stack,exec_env)

def opmod_instr_constr(matches,parser):
    return opmod_t()
