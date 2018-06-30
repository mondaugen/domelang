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
    ([],'-1-1',[-1,-1],None),
    # initial stack, program, final stack, exception to catch
    ([],'0?456?123¦321»¦789»',[0,789],None), # test empty list
    ([],'0?456?1?123¦572»¦321»¦789»',[0,789],None), # test empty list
    ([],'0?456?123¦321»¦1?789¦572»',[0,1,789],None), # test empty list
    ([],' 123 ? 456 ¦ 789 »  ', [123,456],None),
    ([],' 0 ? 456 ¦ 789 »  ', [0,789],None),
    ([],'0?456¦789»',[0,789],None), # test concision
    ([],'?456¦789»',[789],None), # test empty stack
    ([[]],'?456¦789»',[[],789],None), # test empty list
    ([],'1?456?123¦321»¦789»',[1,456,123],None), # test empty list
    # test arithmetic operators
    ([],'-1 1-',[-2],None),
    ([1,2],'+',[3],None),
    ([2,3],'-',[-1],None),
    ([2,3],'×',[6],None),
    ([3,-2],'≤',[0],None),
    ([3,-2],'≥',[1],None),
    ([[3,-2],[1]],'≥',[[1,0]],None),
    ([2,3],'<?10¦20»',[1,10],None),
    ([2,3],'<¬?10¦20 20=?30¦40»',[0,1,30],None),
    ([2,3],'<¬?10¦20 20¬=?30¦40»',[0,0,40],None),
    ([6,2],'÷',[3.0],None),
    ([1,2],'÷',[0.5],None),
    # to get integer, use floor
    ([],'2 3÷⌋',[0],None),
    ([],'2 3÷⌉',[1],None),
    ([],'2 3(4( 5 3(3(÷',[[2/5,3/3,4/3]],None),
    ([],'2 3(4( 5 3(3(÷⌋',[[0,1,1]],None),
    ([],'2 3(-1]',[3],None),
    ([],'0 3()',[3],None),
    ([],'4 3(√',[[2,3**0.5]],None),
    ([],'4 3(√⌉',[[2,2]],None),
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
    ([[1,2],[]],'+',[],None),
    ([[],[1,2]],'+',[],None),
    ([[1,2,3,4,5],[0,2,4],[8,9]],'[',[[8,2,9,4,8]],None),
    ([[[1,2,3,4,5],[-1.,-2.,-3.,-4.,-5.]],[5,7,9],[8,9]],'[',[[[8,2,9,4,8],[8,-2.,9,-4.,8]]],None), 
    ([[1,2,3,4,5],[5,7,9],9], '[', [[9,2,9,4,9]], None),
    ([[1,2,3,4,5],[5,7.4,9],9], '[', [[9,2,9,4,9]], None),
    ([[1,2,3,4,5],[1,3,5,7,-1,-2]],']',[[2,4,1,3,5,4]],None),
    ([[[1,2,3],[4,5,6]],2],']',[[1,2,3]],None),
    ([[[1,2,3],[4,5,6]],2],'∘]',[[3,6]],None),
    ([[[1],[2],[3],[4],[5],[6],[7]],[[1,2,3],[4,5,6]],2],'∘]]',[[[4],[7]]],None),
    ([[[1],[2],[3],[4],[5],[6],[7]],[[1,2,3],[4,5,6]],2],'∘]∘]',
        [[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7]]],None),
    ([[[1,2,3],[4,5,6],[7,8,9]],[[0,2,4,6],[1,3]]],']',[[[1,3,2,1],[5,4],[7,9,8,7]]],None),
    ([[[1,2,3],[4,5,6],[7,8,9]],[[0,2],1]],'∘]',
        [[[[1,3],[4,6],[7,9]],[2,5,8]]],None),
    ([[1,2,3],[[0,0,1,2],[3,4],2]],']',[[[1,1,2,3],[1,2],3]],None),
    ([[1,2,3],[[0.1,0.2,1.3,2.4],[3.9,4.8],2.1]],']',[[[1,1,2,3],[2,3],3]],None),
    ([1],'(',[[1]],None),
    ([1,2],'(',[[1,2]],None),
    ([1,2],'((',[[[1,2]]],None),
    # This is how you make a list of length 1
    ([],'0 2((∘)',[[2]],None),
    ([[1,2],2],'(',[[1,2,2]],None),
    ([[[1,2],[3,4]],2],'(',[[[1,2],[3,4],2]],None),
    ([[[1,2],[3,4]],2],'∘(',[[[1,2,2],[3,4,2]]],None),
    ([[1,2],[3,4]],'(',[[1,2,[3,4]]],None),
    ([[1,2],[3,4]],'∘(',[[1,2,3,4]],None),
    ([[[1,2],[1,2]],[3,4]],'(',[[[1,2],[1,2],[3,4]]],None),
    ([[[1,2],[1,2]],[3,4]],'∘(',[[[1,2,3],[1,2,4]]],None),
    ([[[1,2],[1,2]],[[3,4]]],'∘(',[[[1,2,3,4],[1,2,3,4]]],None),
    ([[[1,2],[1,2]],[[3,4]]],'(',[[[1,2],[1,2],[[3,4]]]],None),
    ([[1,2]],')',[2],None),
    ([[1]],')',[1],None),
    ([[]],')',[],None),
    ([[[1,2],[3,4,5]]],'∘)',[[2,5]],None),
    ([[[1,2],[3,4,5]]],')',[[3,4,5]],None),
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
