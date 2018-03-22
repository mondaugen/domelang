from instruction import *
import common
from itertools import cycle

class _binary_operator_vtable:
    """
    A table of ways to apply a binary operator depending on the argument types.
    """
    def cycle_rhs(l,r,op):
        for i,(x,y) in enumerate(zip(l,cycle(r))):
            l[i]=binary_operator(x,y,op)
        return l
    def nn(l,r,op):
        return op(l,r)
    def nl(l,r,op):
        return [ op(l,x) for x in r ]
    def nL(l,r,op):
        return [ binary_operator(l,x) for x in r ]
    def ln(l,r,op):
        return [ op(x,r) for x in l ]
    def ll(l,r,op):
        return _binary_operator_vtable.cycle_rhs(l,r,op)
    def lL(l,r,op):
        return _binary_operator_vtable.cycle_rhs(l,r,op)
    def Ln(l,r,op):
        return [ binary_operator(x,r) for x in l ]
    def Ll(l,r,op):
        return _binary_operator_vtable.cycle_rhs(l,r,op)
    def LL(l,r,op):
        return _binary_operator_vtable.cycle_rhs(l,r,op)

def _dyad_divide(x,y):
    return x/y

_dyad_table = {
    '+': lambda x,y: x+y,
    '-': lambda x,y: x-y,
    '÷': _dyad_divide,
    '×': lambda x,y: x*y
}

def binary_operator(l,r,op):
    """
    Applies op to l and r depending on their types and sizes.
    op is a function that takes 2 numbers are returns a number.
    l and r are and valid stack item (number, list, list of lists).
    """
    tc=''.join(map(common.typecode,[l,r]))
    return getattr(_binary_operator_vtable,tc)(l,r,op)

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
            stack.append(binary_operator(l,r,self.op))
        instr_t.execute(self,stack,exec_env)

def dyad_instr_constr(matches,parser):
    return dyad_t(_dyad_table[matches[0]])
