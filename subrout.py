from common import *
from instruction import *

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

    name = 'SRSCOPEPUSH'
    def execute(self,stack,exec_env):
        """
        starts a new scope
        """
        exec_env.scopes = subroutscope_t(exec_env.scopes)
        instr_t.execute(self,stack,exec_env)

class srscopepop_instr_t(instr_t):

    name = 'SRSCOPEPOP'
    def execute(self,stack,exec_env):
        """
        Gets rid of the current scope so the routines in it are no longer
        accessible.
        """
        old_scopes = exec_env.scopes
        exec_env.scopes = exec_env.scopes.parent
        del(old_scopes)
        instr_t.execute(self,stack,exec_env)

class subroutdef_t:
    """
    This is created and exists while a subroutine is being parsed.
    It keeps track of the subroutine's name and instructions.
    """
    def __init__(self,name,first_instr):
        self.name = name
        self.first_instr = first_instr
        #self._current_instr = self.first_instr

subroutparse_name = 'SRDEFSTART'

def subroutparse_newdef(name,parser):
    """
    Made available so that the parser can define custom routines with arbitrary
    names.
    """
    # push the last instruction of the routine parser was just working on
    if (parser.last_instr):
        parser.last_instr_stack.append(parser.last_instr)
    # push a new subroutine definition structure by the subroutine's name and
    # with a scope push as first instruction
    parser.cur_subrout_def.append(subroutdef_t(name,srscopepush_instr_t()))
    # set its instruction as last_instr so that the parser will append
    # instructions there
    parser.last_instr = parser.cur_subrout_def[-1].first_instr
    # return None because we don't want parser to append this instruction as
    # we've set a new self.last_instr
    return None

def subroutparse_constr(matches,parser):
    return subroutparse_newdef(matches[1],parser)

class subroutdefinstr_t(instr_t):
    """
    Created when a full definition of a subroutine is finished.
    When executed, this pushes the definition of this subroutine, replacing the
    old definition (if there was one). This is the subroutine that is executed
    by this name until another definition by the same name is pushed.
    """

    name = 'SRDEFEND'
    def __init__(self,name,first_instr):
        """
        name is the name of the routine
        first_instr is the first instruction in its instruction list
        """
        instr_t.__init__(self)
        self.name = name
        self.first_instr = first_instr

    def execute(self,stack,exec_env):
        """
        replaces definition in current scope with this subroutine's definition
        """
        if not exec_env.scopes:
            raise Exception("No scope in execution environment!")
        exec_env.scopes.subroutines[self.name]=self.first_instr
        instr_t.execute(self,stack,exec_env)

def subroutdefinstr_enddef(parser):
    """
    Called when } encountered (canonically).

    Adds a scope pop instruction as the last instruction of the subroutine
    currently being parsed because that scope is discarded when we leave the
    subroutine.

    Then we get the last instruction on the parser's last_instr_stack and we
    continue on with adding instructions to this list. The first instruction we
    add is the subroutdefinstr_t holding the defintion of the most recently
    parsed subroutine.

    Then we pop the subroutdef_t off the def stack because we are done with that
    routine and now need to continue with the next up the stack.

    Done as a function separate from the constr function becuase the parser
    calls this to end the outermost scope.
    """
    # Add scope pop instruction
    parser.last_instr = append(parser.last_instr,srscopepop_instr_t())
    # Get the last instruction from the outer scope before this subroutine
    # definition was started. Don't worry we don't lose the old
    # parser.last_instr because this is also the last instruction in the
    # instruction list held in the first_instr field of subroutdef_t
    if len(parser.last_instr_stack) > 0:
        parser.last_instr = parser.last_instr_stack.pop()
    else:
        # The program should be done at this point, so we put a dummy
        # instruction so the parser has something to append the
        # subroutdefinstr_t to (see what this function returns)
        parser.last_instr = instr_t()
    # pop the last subroutine definition we were just working on, because we are
    # done with it now
    last_def = parser.cur_subrout_def.pop()
    # the return a subroutdefinstr_t containing the name and subroutine from
    # last_def
    # TODO not sure if I can call del on last_def because we still want its
    # inner fields in the new subroutdefinstr_t
    return subroutdefinstr_t(last_def.name,last_def.first_instr)

def subroutdefinstr_constr(matches,parser):
    return subroutdefinstr_enddef(parser)

class subroutexecinstr_t(instr_t):
    """
    Created and appended to instruction list  when @\w encountered (canonically)

    When executed, it searches up the scopes for the closest subroutine
    definition with its name. If such a routine is found, the next instruction
    is saved as the return address and next instruction is set to the first
    instruction of the found subroutine.
    """
    name = 'SREXEC'
    def __init__(self,name):
        instr_t.__init__(self)
        self.name = name

    def execute(self,stack,exec_env):
        # get next instruction by executing superclass's execute function
        instr_t.execute(self,stack,exec_env)
        # search up scope tree to look up subroutine, if key not there or list
        # empty, next_instr is set to None
        scope = exec_env.scopes
        next_instr = None
        while scope:
            if self.name in scope.subroutines.keys():
                next_instr = scope.subroutines[self.name]
                break
            else:
                scope = scope.parent
        if next_instr:
            if exec_env.next_instr:
                exec_env.return_address.append(exec_env.next_instr)
            exec_env.next_instr = next_instr
        # Otherwise we just continue to the next instruction

def subroutexecinstr_create(name):
    return subroutexecinstr_t(name)

def subroutexecinstr_constr(matches,parser):
    return subroutexecinstr_create(matches[1])
