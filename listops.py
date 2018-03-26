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
        if type(y) != list:
            y=[y]
        y.append(x)
        stack=common.stack_push(stack,y)
        instr_t.execute(self,stack,exec_env)

def listpush_instr_contr(matches,parser):
    return listpush_t()

