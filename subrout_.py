class subroutscope_t:
    """
    Contains a set of subroutines valid in a particular scope.
    This is used by the executer to keep track of what routines are in scope
    and to make it easy to "pop" routines that are no longer in scope when a
    routine finishes.
    """
    def __init__(self,parent):
        self.parent = parent
        self.subroutines = dict()

class srscopepush_instr_t(instr_t):

    def execute(self,stack,exec_env):
        """
        starts a new scope
        """
        exec_env.scopes = subroutscope_t(exec_env.scopes)
        instr_t.execute(self,stack,exec_env)

class srscopepop_instr_t(instr_t):

    def execute(self,stack,exec_env):
        """
        Gets rid of the current scope so the routines in it are no longer
        accessible.
        """
        old_scopes = exec_env.scopes
        exec_env.scopes = exec_env.scopes.parent
        del(old_scopes)

class subroutdef_t:
    """
    This is created and exists while a subroutine is being parsed.
    It keeps track of the subroutine's name and instructions.
    """
    def __init__(self,name,first_instr):
        self.name = name
        self.first_instr = first_instr
        #self._current_instr = self.first_instr

def subroutparse_constr(matches,parser):
    # push the last instruction of the routine parser was just working on
    parser.last_instr_stack.append(parser.last_instr)
    # push a new subroutine definition structure by the subroutine's name and
    # with a scope push as first instruction
    parser.cur_subrout_def.append(subroutdef_t(matches[1],srscopepush_instr_t()))
    # set its instruction as last_instr so that the parser will append
    # instructions there
    parser.last_instr = parser.cur_subrout_def[-1].first_instr
    # return None because we don't want parser to append this instruction as
    # we've set a new self.last_instr
    return None

