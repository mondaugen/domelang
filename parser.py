import listops
from common import *
import number
import conditional
from instruction import *
import operators
import indexing
import subrout
import stackop
import registers

# These are stored in the order that they are matched against. The first
# one to match is executed.
# The regular expressions should contain at least 1 group
cmd_parsers = [
    cmd_parser_t(
        number.float_t.name,
        '([-]?\d+\.\d*([eE][-+]?\d+|))',
        number.float_instr_constr
    ),
    cmd_parser_t(
        number.int_t.name,
        '([-]?\d+)',
        number.int_instr_constr
    ),
    cmd_parser_t(
        conditional.if_instr_t.name,
        '(\?)',
        conditional.if_instr_constr
    ),
    cmd_parser_t(
        conditional.else_instr_t.name,
        '(¦)',
        conditional.else_instr_constr
    ),
    cmd_parser_t(
        conditional.endif_instr_t.name,
        '(»)',
        conditional.endif_instr_constr
    ),
    cmd_parser_t(
        'NOP',
        '(\s+)',
        None
    ),
    cmd_parser_t(
        operators.dyad_t.name + '+',
        '(\+)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        operators.dyad_t.name + '-',
        '(-)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        operators.dyad_t.name + '÷',
        '(÷)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        operators.dyad_t.name + '×',
        '(×)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        operators.dyad_t.name + '<',
        '(<)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        operators.dyad_t.name + '>',
        '(>)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        operators.dyad_t.name + '≤',
        '(≤)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        operators.dyad_t.name + '≥',
        '(≥)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        operators.dyad_t.name + '=',
        '(=)',
        operators.dyad_instr_constr
    ),
    cmd_parser_t(
        operators.outerop_t.name,
        '(∘)',
        operators.outerop_instr_constr
    ),
    cmd_parser_t(
        indexing.setat_t.name,
        '(\[)',
        indexing.setat_instr_constr
    ),
    cmd_parser_t(
        indexing.getat_t.name,
        '(\])',
        indexing.getat_instr_constr
    ),
    cmd_parser_t(
        listops.listpush_t.name,
        '(\()',
        listops.listpush_instr_contr
    ),
    cmd_parser_t(
        listops.listpop_t.name,
        '(\))',
        listops.listpop_instr_contr
    ),
    cmd_parser_t(
        operators.monad_t.name+'¬',
        '(¬)',
        operators.monad_instr_constr
    ),
    cmd_parser_t(
        operators.monad_t.name+'⌉',
        '(⌉)',
        operators.monad_instr_constr
    ),
    cmd_parser_t(
        operators.monad_t.name+'⌋',
        '(⌋)',
        operators.monad_instr_constr
    ),
    cmd_parser_t(
        operators.monad_t.name+'√',
        '(√)',
        operators.monad_instr_constr
    ),
    cmd_parser_t(
        subrout.subroutexecinstr_t.name,
        '(@)([a-zA-Z0-9_])',
        subrout.subroutexecinstr_constr
    ),
    cmd_parser_t(
        subrout.subroutparse_name,
        '(\{)([a-zA-Z0-9_])',
        subrout.subroutparse_constr
    ),
    cmd_parser_t(
        subrout.subroutdefinstr_t.name,
        '(\})',
        subrout.subroutdefinstr_constr
    ),
    cmd_parser_t(
        stackop.stack_dupl_t.name,
        '(‡)',
        stackop.stack_dupl_instr_constr
    ),
    cmd_parser_t(
        stackop.stack_swap_t.name,
        '(⇔)',
        stackop.stack_swap_instr_constr
    ),
    cmd_parser_t(
        stackop.stack_drop_t.name,
        '(↓)',
        stackop.stack_drop_instr_constr
    ),
    cmd_parser_t(
        registers.register_push_exec_t.name,
        '(′)([a-zA-Z_])',
        registers.register_push_exec_instr_constr
    ),
    cmd_parser_t(
        registers.register_pop_exec_t.name,
        '(`)([a-zA-Z_])',
        registers.register_pop_exec_instr_constr
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
        # The stack of last instructions, so that when the definition of a new
        # instruction is invoked, the old definition is pushed and saved. When
        # '}' encountered, it is continued.
        self.last_instr_stack=[]
        self.last_instr = None #TODO What is this initially?
        self.cur_subrout_def = []

    
    def parse(self,cmds):
        """
        Parse the commands in string cmds and update the dictionary of lists of
        instruction lists that can be executed by an executer (self.routines). The keys of this
        list are the subroutine names.
        Initially we start on the instruction 'main' (see __init__)
        """
        # When the program runs
        # the first instruction will push the "main" scope which is the
        # outer-most scope.
        subrout.subroutparse_newdef("main",self)
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
        # Finish main which should be the outer-most scope and so there won't be
        # any other first_instr
        first_instr = subrout.subroutdefinstr_enddef(self)
        self.last_instr = first_instr
        if len(self.cur_subrout_def) > 0:
            raise Exception('Some routines have not been completed (missing closing "}" ?)')
        # The last instruction executes the main routine
        self.last_instr = append(self.last_instr,subrout.subroutexecinstr_create("main"))
        return first_instr
