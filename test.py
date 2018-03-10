import parser
import executer

p=parser.parser_t()

progs=[
    # initial stack, program, final stack
    ([],' 123 ? 456 ¦ 789 »  ', [123,456]),
    ([],' 0 ? 456 ¦ 789 »  ', [0,789]),
    ([],'0?456¦789»',[0,789]), # test concision
    ([],'?456¦789»',[789]), # test empty stack
    ([[]],'?456¦789»',[[],789]), # test empty list
]

for st,pr,res in progs:
    ex=executer.exec_t()
    first_instr=p.parse(pr)
    ex.execute(st,first_instr)
    if st == res:
        print("Passed")
    else:
        print("Failed")
    print("\tExpected ",end='')
    print(res,end='')
    print("\tgot ",end='')
    print(st)
