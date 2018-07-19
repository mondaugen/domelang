__doc__="""
Registers

These are like variables but are implemented as stacks. To store something, you
push in on to a register and to retrieve it you pop it. Registers [a-zA-Z_] are for
users, there are also registers with "private" names: these are used to store
the iterates in for-loops and stuff like that.

Parsing

Pushing to a register is indicated with ′a where a is the register name. To
remember, imagine the registers are hanging above the line and it is a ramp the
data goes up into the register. Popping is `a where a is the register. You can
remember it along similar lines.

Executing

The push command simply pushes the last stack item to that register, and the pop
command pops the last stack item from that register and places it on the main
stack. That's it.

"""

from instruction import *

class register_push_exec_t(instr_t):
    """
    Class executing register push instruction.
    """
    name = 'REGPUSH'
    def __init__(self,register_name):
        self.register_name = register_name
        instr_t.__init__(self)

    def execute(self,stack,exec_env):
        if self.register_name in exec_env.registers.keys():
            # If stack already started under that name, append
            exec_env.registers[self.register_name].append(stack.pop())
        else:
            # Otherwise start a new stack
            exec_env.registers[self.register_name] = [stack.pop()]
        instr_t.execute(self,stack,exec_env)

def register_push_exec_instr_constr(matches,parser):
    return register_push_exec_t(matches[1])

class register_pop_exec_t(instr_t):
    """
    Class executing register pop instruction.
    """
    name = 'REGPOP'
    def __init__(self,register_name):
        self.register_name = register_name
        instr_t.__init__(self)

    def execute(self,stack,exec_env):
        if self.register_name in exec_env.registers.keys():
            stack.append(exec_env.registers[self.register_name].pop())
        instr_t.execute(self,stack,exec_env)

def register_pop_exec_instr_constr(matches,parser):
    return register_pop_exec_t(matches[1])
