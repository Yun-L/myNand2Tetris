from parser import Parser
from code_writer import CodeWriter
from command_types import CommandType
from memory_segment_types import MemorySegType
import sys
import os
import glob

"""
Single Arg. Cmds
  CommandType.C_ARITHMETIC
  CommandType.C_LABEL
  CommandType.C_GOTO
  CommandType.C_IF

Double Arg. Cmds
  CommandType.C_PUSH
  CommandType.C_POP
  CommandType.C_FUNCTION
  CommandType.C_CALL
"""

segment_map = {"argument": MemorySegType.M_ARGUMENT,
               "local": MemorySegType.M_LOCAL,
               "static": MemorySegType.M_STATIC,
               "constant": MemorySegType.M_CONSTANT,
               "this": MemorySegType.M_THIS,
               "that": MemorySegType.M_THAT,
               "pointer": MemorySegType.M_POINTER,
               "temp": MemorySegType.M_TEMP}


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <{sys.argv[1]}>")

    files = []
    target_dir = ""
    if sys.argv[1].endswith('.vm'):
        files.append(sys.argv[1])
    elif os.path.isdir(sys.argv[1]):
        files.extend(glob.glob(f"{sys.argv[1]}*.vm"))
        target_dir = sys.argv[1]
    else:
        raise Exception("Error: target must be a .vm file or a directory")

    cw = CodeWriter(target_dir + sys.argv[1].strip("/.vm") + ".asm")

    print(f"Creating {target_dir + sys.argv[1].strip('/.vm') + '.asm'} ...")

    for f in files:
        p = Parser(f)
        cw.file_name = f.split("/")[-1]
        while p.advance():
            if p.command_type == CommandType.C_ARITHMETIC:
                cw.write_arithmetic(p.arg1())
            elif p.command_type == CommandType.C_PUSH:
                cw.write_push_pop(CommandType.C_PUSH,
                                  segment_map[p.arg1()], p.arg2())
            elif p.command_type == CommandType.C_POP:
                cw.write_push_pop(CommandType.C_POP,
                                  segment_map[p.arg1()], p.arg2())
            elif p.command_type == CommandType.C_LABEL:
                cw.write_label(p.arg1())
            elif p.command_type == CommandType.C_GOTO:
                cw.write_goto(p.arg1())
            elif p.command_type == CommandType.C_IF:
                cw.write_if(p.arg1())
            elif p.command_type == CommandType.C_CALL:
                cw.write_call(p.arg1(), p.arg2())
            elif p.command_type == CommandType.C_FUNCTION:
                cw.curr_fn = p.arg1()
                cw.write_function(p.arg1(), p.arg2())
            elif p.command_type == CommandType.C_RETURN:
                cw.write_return()

    print("Success.")
