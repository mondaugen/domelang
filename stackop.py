# Operators modifying the stack

from instruction import *
import copy
import common

class stack_dupl_t(instr_t):
    """
    Double the last stack item with a deep copy.
    """
    name = 'STACKDUPL'
    def __init__(self):
        instr_t.__init__(self)
    def execute(self,stack,exec_env):
        # Only works if something in the stack
        if len(stack) >= 1:
            a=stack.pop()
            b=copy.deepcopy(a)
            stack=common.stack_push(stack,a)
            stack=common.stack_push(stack,b)
        instr_t.execute(self,stack,exec_env)

def stack_dupl_instr_constr(matches,parser):
    return stack_dupl_t()

class stack_swap_t(instr_t):
    """
    Swap the last 2 stack items
    """
    name = 'STACKSWAP'
    def __init__(self):
        instr_t.__init__(self)
    def execute(self,stack,exec_env):
        # Only works if at least 2 items in the stack
        if len(stack) >= 2:
            r=stack.pop()
            l=stack.pop()
            stack=common.stack_push(stack,r)
            stack=common.stack_push(stack,l)
        instr_t.execute(self,stack,exec_env)

def stack_swap_instr_constr(matches,parser):
    return stack_swap_t()

class stack_drop_t(instr_t):
    """
    Discard the last stack item.
    """
    name = 'STACKDROP'
    def __init__(self):
        instr_t.__init__(self)
    def execute(self,stack,exec_env):
        if len(stack) >= 1:
            a=stack.pop()
            del(a)
        instr_t.execute(self,stack,exec_env)

def stack_drop_instr_constr(matches,parser):
    return stack_drop_t()
