from typing import List
from command_types import CommandType
from memory_segment_types import MemorySegType


class CodeWriter(object):
    """Translates VM commands into Hack assembly code"""

    def __init__(self, outfile: str):
        self.__outfile = open(outfile, "w")
        self.__file_name: str = "default"
        self.__EGL_count = 0
        # initialize stack pointer
        self.__write_asm(["@256",
                          "D=A",
                          "@SP",
                          "M=D"])
        return

    def __del__(self):
        self.__outfile.close()
        return

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, file_name: str):
        self.__file_name = file_name
        return

    def __create_EGL_labels(self):
        """
        Returns a tuple of the form '("$EGL.T.xxx", "$EGL.E.xxx")'
        where xxx is an integer globally unique in the resulting program
        """
        base_labels = ("$EGL.T.", "$EGL.E.")
        result = tuple(map(lambda x: x + str(self.__EGL_count), base_labels))
        self.__EGL_count += 1
        return result

    def __write_asm(self, cmds: List[str]):
        buf = "\n".join(cmds) + "\n"
        self.__outfile.write(buf)
        return

    def __write_push(self, segment: MemorySegType, ind: int):
        def push_error(ind: int, segment: MemorySegType):
            raise Exception(f"Error: can't push to index '{ind}' for "
                            f"'{segment}'.")

        # Get value from memory segment, store in D
        if segment == MemorySegType.M_CONSTANT:
            if ind < 0 or ind > 32767:
                push_error(ind, segment)
            self.__write_asm([f"@{ind}",
                              "D=A"])

        elif segment == MemorySegType.M_LOCAL:
            if ind < 0:
                push_error(ind, segment)
            self.__write_asm([f"@{ind}",
                              "D=A",
                              "@LCL",
                              "A=M",
                              "A=D+A",
                              "D=M"])

        elif segment == MemorySegType.M_ARGUMENT:
            if ind < 0:
                push_error(ind, segment)
            self.__write_asm([f"@{ind}",
                              "D=A",
                              "@ARG",
                              "A=M",
                              "A=D+A",
                              "D=M"])

        elif segment == MemorySegType.M_THIS:
            if ind < 0:
                push_error(ind, segment)
            self.__write_asm([f"@{ind}",
                              "D=A",
                              "@THIS",
                              "A=M",
                              "A=D+A",
                              "D=M"])

        elif segment == MemorySegType.M_THAT:
            if ind < 0:
                push_error(ind, segment)
            self.__write_asm([f"@{ind}",
                              "D=A",
                              "@THAT",
                              "A=M",
                              "A=D+A",
                              "D=M"])

        elif segment == MemorySegType.M_POINTER:
            if ind > 1 or ind < 0:
                push_error(ind, segment)
            self.__write_asm([f"@R{3+ind}",
                              "D=A"])

        elif segment == MemorySegType.M_TEMP:
            if ind < 0 or ind > 7:
                push_error(ind, segment)
            self.__write_asm([f"@R{5+ind}",
                              "D=A"])

        elif segment == MemorySegType.M_STATIC:
            self.__write_asm([f"@{self.file_name}.{ind}",
                              "D=M"])

        # Push value in D to stack and increment SP
        self.__write_asm(["@SP",
                          "A=M",
                          "M=D",
                          "@SP",
                          "M=M+1"])
        return

    def __write_pop(self, segment: MemorySegType, ind: int):
        def pop_error(ind: int, segment: MemorySegType):
            raise Exception(f"Error: can't pop to index '{ind}' for "
                            f"'{segment}'.")

        if segment == MemorySegType.M_CONSTANT:
            # Do nothing, Constant has no actual memory space
            raise Exception(f"Error: can't pop to '{segment}'. "
                            "Has no actual memory space.")

        elif segment == MemorySegType.M_LOCAL:
            if ind < 0:
                pop_error(ind, segment)
            self.__write_asm([f"@{ind}",
                              "D=A",
                              "@LCL",
                              "A=M",
                              "A=D+A"])

        elif segment == MemorySegType.M_ARGUMENT:
            if ind < 0:
                pop_error(ind, segment)
            self.__write_asm([f"@{ind}",
                              "D=A",
                              "@ARG",
                              "A=M",
                              "A=D+A"])

        elif segment == MemorySegType.M_THIS:
            if ind < 0:
                pop_error(ind, segment)
            self.__write_asm([f"@{ind}",
                              "D=A",
                              "@THIS",
                              "A=M",
                              "A=D+A"])

        elif segment == MemorySegType.M_THAT:
            if ind < 0:
                pop_error(ind, segment)
            self.__write_asm([f"@{ind}",
                              "D=A",
                              "@THAT",
                              "A=M",
                              "A=D+A"])

        elif segment == MemorySegType.M_POINTER:
            if ind < 0 or ind > 1:
                pop_error(ind, segment)
            self.__write_asm([f"@R{3+ind}"])

        elif segment == MemorySegType.M_TEMP:
            if ind < 0 or ind > 7:
                pop_error(ind, segment)
            self.__write_asm([f"@R{5+ind}"])

        elif segment == MemorySegType.M_STATIC:
            self.__write_asm([f"@{self.file_name}.{ind}"])

        # temporarily store address in R13 and pop stack val to *R13
        self.__write_asm(["D=A",
                          "@R13",
                          "M=D",
                          "@SP",
                          "M=M+1",
                          "D=M",
                          "@R13",
                          "A=M",
                          "M=D"])

    def write_arithmetic(self, command: str):
        if command == "add":
            self.__write_asm(["@SP",
                              "M=M-1",
                              "A=M",
                              "D=M",
                              "@SP",
                              "M=M-1",
                              "A=M",
                              "M=D+M",
                              "@SP",
                              "M=M+1"])
        elif command == "sub":
            self.__write_asm(["@SP",
                              "M=M-1",
                              "A=M",
                              "D=M",
                              "@SP",
                              "M=M-1",
                              "A=M",
                              "M=M-D",
                              "@SP",
                              "M=M+1"])
        elif command == "neg":
            self.__write_asm(["D=0",
                              "@SP",
                              "M=M-1",
                              "A=M",
                              "M=D-M",
                              "@SP",
                              "M=M+1"])
        elif command == "eq":
            labels = self.__create_EGL_labels()
            self.__write_asm(["@SP",
                              "M=M-1",
                              "A=M",
                              "D=M",
                              "@SP",
                              "M=M-1",
                              "A=M",
                              "D=M-D",
                              f"@{labels[0]}",
                              "D;JEQ",
                              "@SP",
                              "A=M",
                              "M=0",
                              f"@{labels[1]}",
                              "0;JMP",
                              f"({labels[0]})",
                              "@SP",
                              "A=M",
                              "M=-1",
                              f"({labels[1]})",
                              "@SP",
                              "M=M+1"])
        elif command == "gt":
            labels = self.__create_EGL_labels()
            self.__write_asm(["@SP",
                              "M=M-1",
                              "A=M",
                              "D=M",
                              "@SP",
                              "M=M-1",
                              "A=M",
                              "D=M-D",
                              f"@{labels[0]}",
                              "D;JGT",
                              "@SP",
                              "A=M",
                              "M=0",
                              f"@{labels[1]}",
                              "0;JMP",
                              f"({labels[0]})",
                              "@SP",
                              "A=M",
                              "M=-1",
                              f"({labels[1]})",
                              "@SP",
                              "M=M+1"])
        elif command == "lt":
            labels = self.__create_EGL_labels()
            self.__write_asm(["@SP",
                              "M=M-1",
                              "A=M",
                              "D=M",
                              "@SP",
                              "M=M-1",
                              "A=M",
                              "D=M-D",
                              f"@{labels[0]}",
                              "D;JLT",
                              "@SP",
                              "A=M",
                              "M=0",
                              f"@{labels[1]}",
                              "0;JMP",
                              f"({labels[0]})",
                              "@SP",
                              "A=M",
                              "M=-1",
                              f"({labels[1]})",
                              "@SP",
                              "M=M+1"])
        elif command == "and":
            self.__write_asm(["@SP",
                              "M=M-1",
                              "A=M",
                              "D=M",
                              "@SP",
                              "M=M-1",
                              "A=M",
                              "M=D&M",
                              "@SP",
                              "M=M+1"])
        elif command == "or":
            self.__write_asm(["@SP",
                              "M=M-1",
                              "A=M",
                              "D=M",
                              "@SP",
                              "M=M-1",
                              "A=M",
                              "M=D|M",
                              "@SP",
                              "M=M+1"])
        elif command == "not":
            self.__write_asm(["@SP",
                              "M=M-1",
                              "A=M",
                              "M=!M",
                              "@SP",
                              "M=M+1"])
        else:
            raise Exception(f"Error: invalid arithmetic command '{command}'.")

    def write_push_pop(self, cmd: CommandType, seg: MemorySegType, ind: int):
        if cmd == CommandType.C_PUSH:
            self.__write_push(seg, ind)
        elif cmd == CommandType.C_POP:
            self.__write_pop(seg, ind)
        else:
            raise Exception(f"Error: '{cmd}' is invalid.")


if __name__ == "__main__":

    cw = CodeWriter("test.asm", "test")

    cw.write_push_pop(CommandType.C_PUSH, MemorySegType.M_CONSTANT, 7)
    cw.write_push_pop(CommandType.C_PUSH, MemorySegType.M_CONSTANT, 8)
    cw.write_arithmetic("add")
