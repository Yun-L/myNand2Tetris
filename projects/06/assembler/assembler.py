__author__ = "Yun-L"

import sys

from parser import Parser
from code import Code

OPCODE_LENGTH = 16


def to_binary(num):
    num = int(num)
    binary = ""

    while num > 0:
        binary = str(num % 2) + binary
        num = num // 2

    return binary


def a_cmd_code(num):
    binary_a = to_binary(num)

    if len(binary_a) >= OPCODE_LENGTH:
        raise Exception(
            "[{}] is too large to load to A".format(num))

    return "0"*(OPCODE_LENGTH-len(binary_a)) + binary_a


if __name__ == "__main__":

    file_location = sys.argv[1]
    dest_file = sys.argv[2]

    # Initialize symbol table and predefined symbol values
    symbol_table = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "SCREEN": 16384,
        "KBD": 24576
    }

    # Find all L_commands and add to symbol table

    parse1 = Parser(file_location)

    address_counter = -1

    while parse1.has_more_commands:
        parse1.advance()

        if parse1.command_type == "A_COMMAND" \
           or parse1.command_type == "C_COMMAND":

            address_counter += 1

        if parse1.command_type == "L_COMMAND":

            if parse1.symbol in symbol_table:

                raise Exception("({}) symbol occurs more than once".format(
                    parse1.symbol))

            symbol_table[parse1.symbol] = address_counter + 1

    # Translate all assembly to opcode

    parse2 = Parser(file_location)

    variable_addr_counter = 16

    with open(dest_file, "w") as outfile:

        while parse2.has_more_commands:
            parse2.advance()

            if parse2.command_type == "A_COMMAND":
                a_value = parse2.symbol

                if len(a_value) < 1:
                    raise Exception("No value found for A_COMMAND")

                if a_value.isnumeric():

                    outfile.write(a_cmd_code(a_value) + "\n")
                else:

                    if a_value not in symbol_table:
                        symbol_table[a_value] = variable_addr_counter

                        variable_addr_counter += 1

                    outfile.write(a_cmd_code(symbol_table[a_value]) + "\n")

            elif parse2.command_type == "C_COMMAND":
                dest = parse2.dest
                comp = parse2.comp
                jump = parse2.jump

                c_code = Code(parse2.dest, parse2.jump, parse2.comp)

                outfile.write("111" + c_code.comp +
                              c_code.dest + c_code.jump + "\n")
