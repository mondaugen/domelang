import subrout

class exec_t:
    """
    The run-time execution environment.
    """

    def __init__(self):
        self.return_address = []
        self.next_instr = None
        self.flgs=[]
        self.rqst_flgs=[]
        self.routines = None
        self.registers = dict()
        self.scopes = None

    def set_routines(self,instrd):
        """
        instrd is a dictionary of lists of instruction lists whose keys are the names of
        the subroutines.
        """
        self.routines = instrd

    def execute(self,stack,show_stack=False):
        """
        Execute instructions, affecting the stack.
        This starts by default in the subroutine "main" and calls other
        subroutines as they are encountered.
        """
        if not self.routines:
            raise Exception('No routines to execute')
        self.next_instr = self.routines['main'][-1]
        while self.next_instr:
            self.next_instr.execute(stack,self)
            if show_stack:
                print(stack)
            # Remove set flags
            self.flgs=[]
            # Check if flag sets requested and put them in flags
            for flg in self.rqst_flgs:
                self.flgs.append(flg)
            self.rqst_flgs=[]
            # If no more next_instr, check if there's a return address, and jump
            # there if there is
            if (not self.next_instr) and (len(self.return_address) > 0):
                self.next_instr = self.return_address.pop()
        # No more instructions, we are done
        return

