from common import *
import number
import conditional
from instruction import *
import operators

# These are stored in the order that they are matched against. The first
# one to match is executed.
# The regular expressions should contain at least 1 group
cmd_parsers = [
    cmd_parser_t(
        'FLOAT',
        '([-+]?\d+\.\d*([eE][-+]?\d+|))',
        number.float_instr_constr
    ),
    cmd_parser_t(
        'INT',
        '([-+]?\d+)',
        number.int_instr_constr
    ),
    cmd_parser_t(
        'IF',
        '(\?)',
        conditional.if_instr_constr
    ),
    cmd_parser_t(
        'ELSE',
        '(¦)',
        conditional.else_instr_constr
    ),
    cmd_parser_t(
        'ENDIF',
        '(»)',
        conditional.endif_instr_constr
    ),
    cmd_parser_t(
        'NOP',
        '(\s+)',
        None
    ),
    cmd_parser_t(
        'PLUS',
        '(\+)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        'MINUS',
        '(-)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        'DIVIDE',
        '(÷)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        'TIMES',
        '(×)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        'OUTER',
        '(∘)',
        operators.outerop_instr_constr
    ),
]

class parser_t:
    """
    A parser of a domelang program.
    """

    def __init__(self):
        # A stack of if statments, the top one currently being parsed.
        self.ifs = None
    
    def parse(self,cmds):
        """
        Parse the commands in string cmds and return the head of a list of
        instructions that can be executed by an executer.
        """
        # The first instruction in the program
        first_instr=None
        # The last instruction in the program
        last_instr=None

        while cmds:
            matched = False
            for cmdp in cmd_parsers:
                m=cmdp.regex.match(cmds)
                if m:
                    print(m)
                    print(m.groups())
                    newinstr = None
                    if cmdp.instr_constr:
                        newinstr = cmdp.instr_constr(m.groups(),self)
                    if newinstr:
                        # check if newinstr because some don't return
                        # instructions, like NOP
                        if last_instr:
                            last_instr = append(last_instr,newinstr)
                        else:
                            last_instr = newinstr
                        if not first_instr:
                            first_instr = last_instr
                    cmds=cmds[m.end(0):]
                    matched = True
                    break
            if not matched:
                print("Error: no match for %s" % (cmds,))
                break
        return first_instr

