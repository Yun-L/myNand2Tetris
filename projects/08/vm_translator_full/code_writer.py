from typing import List
from command_types import CommandType
from memory_segment_types import MemorySegType


class CodeWriter(object):
    """Translates VM commands into Hack assembly code"""

    def __init__(self, outfile: str):
        self.__outfile = open(outfile, "w")
        self.__file_name: str = "default"
        self.__EGL_count = 0
        self.__return_count = 0
        self.__curr_fn = None
        # Bootstrapping code
        self.__write_asm(["@256",
                          "D=A",
                          "@SP",
                          "M=D"])
        self.write_call("Sys.init", 0)
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

    @property
    def curr_fn(self):
        return self.__curr_fn

    @curr_fn.setter
    def curr_fn(self, curr_fn: str):
        self.__curr_fn = curr_fn
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
                              "D=M"])

        elif segment == MemorySegType.M_TEMP:
            if ind < 0 or ind > 7:
                push_error(ind, segment)
            self.__write_asm([f"@R{5+ind}",
                              "D=M"])

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
                          "M=M-1",
                          "A=M",
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
        return

    def write_push_pop(self, cmd: CommandType, seg: MemorySegType, ind: int):
        if cmd == CommandType.C_PUSH:
            self.__write_push(seg, ind)
        elif cmd == CommandType.C_POP:
            self.__write_pop(seg, ind)
        else:
            raise Exception(f"Error: '{cmd}' is invalid.")
        return

    def write_label(self, label: str):
        self.__write_asm([f"({self.__curr_fn}:{label})"])
        return

    def write_goto(self, label: str):
        self.__write_asm([f"@{self.__curr_fn}:{label}",
                          "0;JMP"])
        return

    def write_if(self, label: str):
        self.__write_asm(["@SP",
                          "M=M-1",
                          "A=M",
                          "D=M",
                          f"@{self.__curr_fn}:{label}",
                          "D;JNE"])
        return

    def write_call(self, fn_name: str, num_args: int):
        def push_addr(addr: str, deref: str):
            # deref should be A for address, M for value
            self.__write_asm([f"@{addr}",
                              f"D={deref}",
                              "@SP",
                              "A=M",
                              "M=D",
                              "@SP",
                              "M=M+1"])
            return

        # push previous frame's addresses
        push_addr(f"{self.__curr_fn}:return.{self.__return_count}", "A")
        push_addr("LCL", "M")
        push_addr("ARG", "M")
        push_addr("THIS", "M")
        push_addr("THAT", "M")
        # set up new frame
        self.__write_asm(
            ["@SP",
             "D=M",
             "@LCL",  # reposition LCL
             "M=D",
             f"@{num_args+5}",
             "D=D-A",
             "@ARG",  # reposition ARG
             "M=D",
             f"@{fn_name}",
             "0;JMP",  # jump to called function
             f"({self.__curr_fn}:return.{self.__return_count})"])

        self.__return_count += 1
        return

    def write_return(self):
        self.__write_asm(["@LCL",
                          "D=M",
                          "@FRAME",
                          "M=D",
                          "@5",
                          "A=D-A",
                          "D=M",
                          "@R14",
                          "M=D"])  # temp. save ret addr in R13

        self.__write_pop(MemorySegType.M_ARGUMENT, 0)

        # restore calling function addresses
        self.__write_asm(["@ARG",
                          "D=M+1",
                          "@SP",
                          "M=D",
                          "@FRAME",
                          "M=M-1",
                          "A=M",
                          "D=M",
                          "@THAT",
                          "M=D",
                          "@FRAME",
                          "M=M-1",
                          "A=M",
                          "D=M",
                          "@THIS",
                          "M=D",
                          "@FRAME",
                          "M=M-1",
                          "A=M",
                          "D=M",
                          "@ARG",
                          "M=D",
                          "@FRAME",
                          "M=M-1",
                          "A=M",
                          "D=M",
                          "@LCL",
                          "M=D"])

        # return to calling function
        self.__write_asm(["@R14",
                          "A=M",
                          "0;JMP"])
        return

    def write_function(self, fn_name: str, num_locals: int):

        self.__write_asm([f"({fn_name})"])

        for i in range(num_locals):
            # make space for and initialize local variables to 0
            self.__write_asm(["@SP",
                              "A=M",
                              "M=0",
                              "@SP",
                              "M=M+1"])

        return


if __name__ == "__main__":
    # Test
    cw = CodeWriter("test.asm", "test")

    cw.write_push_pop(CommandType.C_PUSH, MemorySegType.M_CONSTANT, 7)
    cw.write_push_pop(CommandType.C_PUSH, MemorySegType.M_CONSTANT, 8)
    cw.write_arithmetic("add")
