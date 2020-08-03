from custom_types import MemorySegType, ArithCMD


class VMWriter():
    """ Writes VM commands into a file """

    def __init__(self, output_file_stream):
        self.__output_file_stream = output_file_stream
        return

    def write_push(self, segment: MemorySegType, index: int):
        self.__output_file_stream.write(f"push {segment.value} {index}\n")
        return

    def write_pop(self, segment: MemorySegType, index: int):
        self.__output_file_stream.write(f"pop {segment.value} {index}\n")
        return

    def write_arithmetic(self, command: ArithCMD):
        self.__output_file_stream.write(command.value + "\n")
        return

    def write_label(self, label):
        self.__output_file_stream.write(f"label {label}\n")
        return

    def write_goto(self, label):
        self.__output_file_stream.write(f"goto {label}\n")
        return

    def write_if(self, label):
        self.__output_file_stream.write(f"if-goto {label}\n")
        return

    def write_call(self, name, num_args):
        self.__output_file_stream.write(f"call {name} {num_args}\n")
        return

    def write_function(self, name, num_locals):
        self.__output_file_stream.write(f"function {name} {num_locals}\n")
        return

    def write_return(self):
        self.__output_file_stream.write("return\n")
        return


if __name__ == "__main__":
    with open("./test.vm", "w") as outfile:
        o = VMWriter(outfile)
        o.write_push(MemorySegType.THIS, 2)
        o.write_push(MemorySegType.ARGUMENT, 1)
        o.write_arithmetic(ArithCMD.ADD)
        o.write_push(MemorySegType.ARGUMENT, 0)
        o.write_push(MemorySegType.ARGUMENT, 1)
        o.write_push(MemorySegType.CONSTANT, 1)
        o.write_call("Math.multiply", 2)
        o.write_call("BankAccount.commision", 2)
        o.write_arithmetic(ArithCMD.SUB)
        o.write_pop(MemorySegType.THIS, 2)
        o.write_return()
