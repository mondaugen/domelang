import listops
from common import *
import number
import conditional
from instruction import *
import operators
import indexing
import subrout
import stackop

# These are stored in the order that they are matched against. The first
# one to match is executed.
# The regular expressions should contain at least 1 group
cmd_parsers = [
    cmd_parser_t(
        'FLOAT',
        '([-]?\d+\.\d*([eE][-+]?\d+|))',
        number.float_instr_constr
    ),
    cmd_parser_t(
        'INT',
        '([-]?\d+)',
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
        'LT',
        '(<)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        'GT',
        '(>)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        'LTE',
        '(≤)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        'GTE',
        '(≥)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        'EQUALS',
        '(=)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        'OUTER',
        '(∘)',
        operators.outerop_instr_constr
    ),
    cmd_parser_t(
        'SETAT',
        '(\[)',
        indexing.setat_instr_constr
    ),
    cmd_parser_t(
        'GETAT',
        '(\])',
        indexing.getat_instr_constr
    ),
    cmd_parser_t(
        'LISTPUSH',
        '(\()',
        listops.listpush_instr_contr
    ),
    cmd_parser_t(
        'LISTPOP',
        '(\))',
        listops.listpop_instr_contr
    ),
    cmd_parser_t(
        'NOT',
        '(¬)',
        operators.monad_instr_constr
    ),
    cmd_parser_t(
        'CEIL',
        '(⌉)',
        operators.monad_instr_constr
    ),
    cmd_parser_t(
        'FLOOR',
        '(⌋)',
        operators.monad_instr_constr
    ),
    cmd_parser_t(
        'SQRT',
        '(√)',
        operators.monad_instr_constr
    ),
    cmd_parser_t(
        'SREXEC',
        '(@)([a-zA-Z0-9_])',
        subrout.subroutexec_instr_constr
    ),
    cmd_parser_t(
        'SRDEFSTART',
        '(\{)([a-zA-Z0-9_])',
        subrout.subroutparse_constr
    ),
    cmd_parser_t(
        'SRDEFEND',
        '(\})',
        subrout.subroutendparse_constr
    ),
    cmd_parser_t(
        'STACKDUPL',
        '(‡)',
        stackop.stack_dupl_instr_constr
    ),
    cmd_parser_t(
        'STACKSWAP',
        '(⇔)',
        stackop.stack_swap_instr_constr
    ),
    cmd_parser_t(
        'STACKDROP',
        '(↓)',
        stackop.stack_drop_instr_constr
    ),
]

class parser_t:
    """
    A parser of a domelang program.
    """

    def __init__(self):
        # A stack of if statments, the top one currently being parsed.
        self.ifs = None
        # The dictionary of subroutines. This is a class member because the
        # parser preserves its state between calls to parse.
        # A subroutine must contain at least 1 instruction
        self.routines={'main':[instr_t()]}
        # The stack of last instructions, so that when the definition of a new
        # instruction is invoked, the old definition is pushed and saved. When
        # '}' encountered, it is continued.
        self.last_instr_stack=[]
        self.last_instr = self.routines['main'][-1]
    
    def parse(self,cmds):
        """
        Parse the commands in string cmds and update the dictionary of lists of
        instruction lists that can be executed by an executer (self.routines). The keys of this
        list are the subroutine names.
        Initially we start on the instruction 'main'
        """

        while cmds:
            matched = False
            for cmdp in cmd_parsers:
                # match the instruction token(s)
                m=cmdp.regex.match(cmds)
                if m:
                    print(m)
                    print(m.re.pattern)
                    print(m.groups())
                    newinstr = None
                    if cmdp.instr_constr:
                        newinstr = cmdp.instr_constr(m.groups(),self)
                    if not self.last_instr:
                        # This means that parsing was prematurely terminated, so
                        # we quit
                        return
                    if newinstr:
                        # check if newinstr because some don't return
                        # instructions, like NOP
                        self.last_instr = append(self.last_instr,newinstr)
                    cmds=cmds[m.end(0):]
                    matched = True
                    break
            if not matched:
                print("Error: no match for %s" % (cmds,))
                break
