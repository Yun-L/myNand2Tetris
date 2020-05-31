from command_types import CommandType


class Parser(object):
    """
    Encapsulates access to the input code. Reads a VM command, parses it, and
    provides convenient access to its components. In addition, Removes all
    white space and comments.
    """

    def __init__(self, infile):
        self.__command_stream = open(infile, "r")
        self.__current_command: CommandType = None

        return

    def __del__(self):
        self.__command_stream.close()

    @property
    def has_more_commands(self) -> bool:
        file_curr_line = self.__command_stream.tell()

        while True:

            peek_next = self.__command_stream.readline()

            if peek_next == "":
                self.__command_stream.seek(file_curr_line)
                return False

            peek_next = self.__remove_comments(peek_next)

            if peek_next.isspace() or peek_next == "":
                continue
            else:
                self.__command_stream.seek(file_curr_line)
                return True

    @property
    def curr_command(self):
        return self.__current_command

    @property
    def command_type(self) -> CommandType:
        mapping = {"push": CommandType.C_PUSH,
                   "pop": CommandType.C_POP,
                   "add": CommandType.C_ARITHMETIC,
                   "sub": CommandType.C_ARITHMETIC,
                   "neg": CommandType.C_ARITHMETIC,
                   "eq": CommandType.C_ARITHMETIC,
                   "gt": CommandType.C_ARITHMETIC,
                   "lt": CommandType.C_ARITHMETIC,
                   "and": CommandType.C_ARITHMETIC,
                   "or": CommandType.C_ARITHMETIC,
                   "not": CommandType.C_ARITHMETIC,
                   "label": CommandType.C_LABEL,
                   "goto": CommandType.C_GOTO,
                   "if-goto": CommandType.C_IF,
                   "function": CommandType.C_FUNCTION,
                   "call": CommandType.C_CALL,
                   "return": CommandType.C_RETURN}

        cmd = self.__current_command.split()[0]
        cmd_type = mapping.get(cmd)

        if cmd_type is None:
            raise Exception(f"Error: No command type for '{cmd}'")

        return cmd_type

    def __remove_comments(self, cmd):
        """
        Takes an input string and returns the same string but without the
        comments (substring starting with '//')
        """
        temp_cmd = cmd
        for i in range(len(cmd) - 1):
            if temp_cmd[i] == "/" and temp_cmd[i + 1] == "/":
                temp_cmd = temp_cmd[:i]
                break
        return temp_cmd

    def advance(self) -> bool:
        """
        Sets current_command to the next command. Immediately returns if no
        more commands left.
        """
        if not self.has_more_commands:
            return False

        while True:
            curr_line = self.__command_stream.readline()
            curr_line = self.__remove_comments(curr_line)

            if not curr_line.isspace() and len(curr_line) > 0:
                break

        self.__current_command = curr_line.strip("\t\n ")
        return True

    def arg1(self) -> str:
        """
        Returns the first argument of the current command. C_ARITHMETIC
        should just return the command itself. Should not be called for
        C_RETURN.
        """

        args = self.__current_command.split()

        if self.command_type == CommandType.C_RETURN:
            raise Exception("Error: arg1 should not be called for cmd type "
                            f"{self.command_type}")
        elif self.command_type == CommandType.C_ARITHMETIC:
            return args[0]
        else:
            if len(args) < 2:
                raise Exception("Error: no argument found for "
                                f"{self.__current_command.split()}")
            return args[1]

    def arg2(self) -> int:
        """
        Returns second argument of current command. Should only be called if
        Current command is one of the tips in valid_cmds
        """

        valid_cmds = [CommandType.C_PUSH,
                      CommandType.C_POP,
                      CommandType.C_FUNCTION,
                      CommandType.C_CALL]

        args = self.__current_command.split()

        if self.command_type not in valid_cmds:
            raise Exception("Error: arg2 should not be called for cmd type "
                            f"{self.command_type}")
        else:
            if len(args) < 3:
                raise Exception("Error: no argument found for "
                                f"{self.__current_command.split()}")
            return int(args[2])


if __name__ == "__main__":

    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <{sys.argv[1]}>")

    p = Parser(sys.argv[1])

    w_arg1 = [CommandType.C_ARITHMETIC,
              CommandType.C_PUSH,
              CommandType.C_POP,
              CommandType.C_LABEL,
              CommandType.C_GOTO,
              CommandType.C_IF,
              CommandType.C_FUNCTION,
              CommandType.C_CALL]

    w_arg2 = [CommandType.C_PUSH,
              CommandType.C_POP,
              CommandType.C_FUNCTION,
              CommandType.C_CALL]

    while p.advance():
        print(f"{p.curr_command} : {p.command_type}", end=" ")
        if p.command_type in w_arg1:
            print(f": arg1='{p.arg1()}'", end=" ")
        if p.command_type in w_arg2:
            print(f": arg2='{p.arg2()}'", end=" ")

        print()
