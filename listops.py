from instruction import *

class listpop_t(instr_t):
    def execute(self,stack,exec_env):
        if len(stack) < 1:
            instr_t.execute(self,stack,exec_env)
            return
        if type(stack[-1]) != list:
            instr_t.execute(self,stack,exec_env)
            return
        x=stack.pop()
        stack.append(x[:-1])
        stack.append(x[-1])
        instr_t.execute(self,stack,exec_env)

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
            stack.append([x])
            instr_t.execute(self,stack,exec_env)
            return
        y=stack.pop()
        if type(y) != list:
            y=[y]
        y.append(x)
        stack.append(y)
        instr_t.execute(self,stack,exec_env)

def listpush_instr_contr(matches,parser):
    return listpush_t()

