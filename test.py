import parser
import executer

p=parser.parser_t()

class NonException(Exception):
    """
    If this trips, it was because the test wasn't supposed to produce an
    exception but did.
    """
    def __init__(self):
        BaseException.__init__(self)

progs=[
    # initial stack, program, final stack, exception to catch
    ([],' 123 ? 456 ¦ 789 »  ', [123,456],None),
    ([],' 0 ? 456 ¦ 789 »  ', [0,789],None),
    ([],'0?456¦789»',[0,789],None), # test concision
    ([],'?456¦789»',[789],None), # test empty stack
    ([[]],'?456¦789»',[[],789],None), # test empty list
    # test arithmetic operators
    ([1,2],'+',[3],None),
    ([2,3],'-',[-1],None),
    ([2,3],'×',[6],None),
    # to get integer, use floor
    ([6,2],'÷',[3.0],None),
    ([1,2],'÷',[0.5],None),
    ([[1,2,3],4],'÷',[[1/4,2/4,3/4]],None),
    # divide by 0 is a killa, but is caught
    # TODO need to specify what exception to catch, otherwise it can't really
    # fail if there's an error
    ([1,0],'÷',[float('inf')],ZeroDivisionError),
    ([[1,2,3],[4,5]],'÷',[[1/4,2/5,3/4]],None),
    ([[1,2,3],[[4,5],[6,7]]],'÷',[[[1/4,1/5],[2/6,2/7],[3/4,3/5]]],None),
    ([[[1,2,3]],[[4,5],[6,7]]],'÷',[[[1/4,2/5,3/4]]],None),
    ([[[4,5],[6,7]],[1,2,3]],'÷',[[[4/1,5/1],[6/2,7/2]]],None),
    ([[1,2],[3,4,5]],'∘+',[[[4,5,6],[5,6,7]]],None),
    ([[1,2],[3,4,5]],'+',[[4,6]],None),
]

passed=True
for st,pr,res,excpt in progs:
    ex=executer.exec_t()
    first_instr=p.parse(pr)
    def _inner(passed):
        # TODO: Why does passed have to get passed in but not the others?
        ex.execute(st,first_instr)
        if st == res:
            print("Passed")
        else:
            print("Failed")
            passed &= False
        print("\tExpected ",end='')
        print(res,end='')
        print("\tgot ",end='')
        print(st)
        return passed
    if excpt:
        try:
            passed=_inner(passed)
            passed &= False
            print("Failed")
        except excpt as e:
            print("Passed")
            print("Caught exception: ",end="")
            print(e)
    else:
        passed=_inner(passed)

print()
if passed:
    print("Tests PASSED.")
else:
    print("Tests FAILED.")
