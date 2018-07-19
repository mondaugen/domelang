from instruction import *

class float_t(instr_t):
    name = 'FLOAT'
    def __init__(self,f):
        instr_t.__init__(self)
        self.f = f
    def execute(self,stack,exec_env):
        stack.append(self.f)
        instr_t.execute(self,stack,exec_env)

def float_instr_constr(matches,parser):
    return float_t(float(matches[0]))

class int_t(instr_t):
    name = 'INT'
    def __init__(self,i):
        instr_t.__init__(self)
        self.i = i
    def execute(self,stack,exec_env):
        stack.append(self.i)
        instr_t.execute(self,stack,exec_env)

def int_instr_constr(matches,parser):
    return int_t(int(matches[0]))
