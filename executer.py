class exec_t:
    """
    The run-time execution environment.
    """

    def __init__(self):
        self.return_address = None
        self.next_instr = None

    def execute(self,stack,instr):
        """
        Execute instructions, affecting the stack.
        """
        self.next_instr = instr
        while self.next_instr:
            self.next_instr.execute(stack,self)
            # If no more next_instr, check if there's a return address, and jump
            # there if there is
            if (not self.next_instr) and self.return_address:
                self.next_instr,self.return_address = pop(self.return_address)
        # No more instructions, we are done
        return

