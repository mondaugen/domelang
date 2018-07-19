import re

class instr_t:
    """
    An instruction.
    """

    # All instances have this name, subclasses override with their method name
    name = 'INSTR'

    def __init__(self):
        # The next instruction, named this way to work with list append, prepend
        # and pop "macros"
        self.next = None

    def execute(self,stack,exec_env):
        """
        Passed the execution environment, and specifies the "address" of the
        next instruction to execute.
        Instructions override this if they need different functionality (which
        is true for most instructions).
        However, most instructions will simply just move on to the next
        instruction, so most instructions should call
        instr_t.execute(self,stack,exec_env) at the end of their call.
        Exceptions to this trend are instructions like "if" that need to jump to
        particular instructions depending on the contents of the stack.
        """
        exec_env.next_instr = self.next

    def __str__(self):
        return self.name

class cmd_parser_t:
    """
    A description of how to go from the character representation of instructions
    and operations to their implementation.
    """
    def __init__(self,name,regex,instr_constr):
        self.name = name
        self.regex = re.compile(regex)
        self.instr_constr = instr_constr

