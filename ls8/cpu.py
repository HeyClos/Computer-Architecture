"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.branch_table = object()
        self.reg[7] = 0xf4 #244

    def CALL(self, *args):
        operand_a = args[0]
        operand_b = args[1]

        return_addr = operand_b

        self.reg[7] -= 1
        self.ram[self.reg[7]] = return_addr

        reg_num = self.ram[operand_a]
        subroutine_addr = self.reg[reg_num]

        self.pc = subroutine_addr
        '''
        index_to_go = self.reg[operand_a]
        save_return_index = operand_b

        self.reg[7] -= 1
        self.ram[self.reg[7]] = save_return_index
        self.pc = index_to_go'''

    def RET(self, *args):
        address = self.reg[7]
        self.pc = self.ram[address]
        self.reg[7] += 1

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        with open(filename) as file:
            for i in file:
                command_split = i.split("#")
                instruction = command_split[0]

                if instruction == "":
                    continue

                first_bit = instruction[0]

                if first_bit == "0" or first_bit == "1":
                    self.ram[address] = int(instruction[:8], 2)
                    address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
            
        
    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            ir = self.ram_read(self.pc)  # Instruction register

            if ir == LDI:
                print("Hello!")
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == PRN:
                value = self.reg[operand_a]
                print(value)
                self.pc += 2
                # reg_num = self.ram[self.pc + 1]
                # value = self.ram[self.pc + 2]
                # self.reg[reg_num] = value
                # self.pc += 3
            elif ir == MUL:
                # Multiply the values in two registers together and store the result in registerA.
                mul_value = self.reg[operand_a] * self.reg[operand_b]
                self.reg[operand_a] = mul_value
                self.pc += 3

            elif ir == PUSH:
                self.reg[7] -= 1

                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]  # <-- this is the value that we want to push

                # Figure out where to store it
                top_of_stack_addr = self.reg[7]

                # Store it
                self.ram[top_of_stack_addr] = value

                self.pc += 2

            elif ir == POP:
                value = self.ram[self.reg[7]]
                self.reg[operand_a] = value

                self.pc += 2
                self.reg[7] += 1

            elif ir == HLT:
                running = False

            else:
                print(f'Unknown instruction {ir} at self.pc {self.pc}')
                sys.exit(1)

