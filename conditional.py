from common import *
from instruction import *

class if_instr_t(instr_t):
    def __init__(self):
        instr_t.__init__(self)
        self.else_instr = None
        self.endif_instr = None
    def execute(self,stack,exec_env):
        if len(stack) > 0 and is_true(stack[-1]):
            exec_env.next_instr = self.next
        else:
            if self.else_instr:
                exec_env.next_instr = self.else_instr.next
            elif self.endif_instr:
                exec_env.next_instr = self.endif_instr.next
            else:
                exec_env.next_instr = None

def if_instr_constr(matches,parser):
    newif = if_instr_t()
    parser.ifs = prepend(parser.ifs,newif)
    return newif

class else_instr_t(instr_t):
    def __init__(self,if_instr):
        """
        if_instr is the "if" this "else" instruction/statement belongs to
        """
        instr_t.__init__(self)
        self.if_instr = if_instr
        self.if_instr.else_instr = self
    def execute(self,stack,exec_env):
        # If we execute this instruction, it means we were in the true clause of
        # the if statement, so we jump to the instruction after the endif
        if self.if_instr and self.if_instr.endif_instr:
            exec_env.next_instr = self.if_instr.endif_instr.next
        else:
            exec_env.next_instr

def else_instr_constr(matches,parser):
    return else_instr_t(parser.ifs)

class endif_instr_t(instr_t):
    """
    If this is executed it means we did the false clause of the if statement so
    we finish by going to the next instruction following this instruction (we
    don't override execute because that's just what it does).
    """
    def __init__(self,if_instr):
        instr_t.__init__(self)
        self.if_instr = if_instr
        self.if_instr.endif_instr = self

def endif_instr_constr(matches,parser):
    # else or endif statements after this should use the next if on the if stack
    oldif,parser.ifs = pop(parser.ifs)
    return endif_instr_t(oldif)
