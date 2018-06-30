__doc__="""
Subroutines

Parsing:
The way this works is when ({)([a-z]) is encountered by the parser, it pushes
the current subroutine and changes to
start placing instructions under the key \2 (the match that is ([a-z])). When
'}' is encountered, it returns to the previous subroutine and parses. If that
subroutine is the last one on the stack, parsing is halted prematurely.

Execution:
The executor is passed to the instruction contructor, so if a subroutine is
found, this pushes the next
instruction on the return stack and sets the next instruction to the first
instruction of the subroutine. If no subroutine is found it is as if NOP is
executed.
"""

from instruction import *

class subroutexec_t(instr_t):
    """
    Class executing subroutines.
    """
    def __init__(self,subroutine_name):
        self.subroutine_name = subroutine_name
        instr_t.__init__(self)

    def execute(self,stack,exec_env):
        # get next instruction
        instr_t.execute(self,stack,exec_env)
        # look up subroutine, if key not there or list empty, next_instr is set
        # to None
        try:
            next_instr_list = exec_env.routines[self.subroutine_name]
        except KeyError:
            next_instr_list = []
        try:
            # Use the most recent subroutine definition (use SRPOP to get rid of
            # it)
            next_instr = next_instr_list[-1]
        except IndexError:
            next_instr = None
        # If next instruction found, push the current next_instr as the return
        # address (if not None) and update next_instr to the found instruction
        if next_instr:
            if exec_env.next_instr:
                exec_env.return_address.append(exec_env.next_instr)
            exec_env.next_instr = next_instr
        # Otherwise we just continue to the next instruction

def subroutexec_instr_constr(matches,parser):
    return subroutexec_t(matches[1])

def subroutparse_constr(matches,parser):
    """Called when it was indicated to start defining an instruction. """
    # push the last instruction of the routine parser was just working on
    parser.last_instr_stack.append(parser.last_instr)
    # if no routine by this name, add a new entry to the dictionary
    if matches[1] not in parser.routines.keys():
        parser.routines[matches[1]]=[]
    # add dummy first instruction (subroutines must contain at least 1
    # instruction)
    parser.routines[matches[1]].append(instr_t())
    # set this as the new last instruction to which instructions will be
    # appended
    parser.last_instr = parser.routines[matches[1]][-1]
    # return None because we don't want parser to append this instruction as
    # we've set a new self.last_instr
    return None

def subroutendparse_constr(matches,parser):
    """Called when we've finished defining a subroutine"""
    try:
        parser.last_instr = parser.last_instr_stack.pop()
    except IndexError:
        # No more instructions
        parser.last_instr = None
    return None
