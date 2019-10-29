__author__ = "Yun-L"


class Parser(object):
    """Breaks each assembly command into its underlying fields and symbols"""

    def __init__(self, filename):

        self.command_stream = open(filename, "r")
        self.current_command = None

    def __del__(self):
        self.command_stream.close()

    @property
    def command_type(self):
        """Returns string 'A_COMMAND' | 'C_COMMAND' | 'L_COMMAND'"""
        if self.current_command[0] == "@":
            return "A_COMMAND"
        elif self.current_command[0] == "(":
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    @property
    def symbol(self):
        if self.command_type == "C_COMMAND":
            raise Exception("Incorrect Type")

        return self.current_command.strip("()@")

    @property
    def dest(self):
        if self.command_type != "C_COMMAND":
            raise Exception("Incorrect Type")

        delim_ind = self.current_command.find("=")
        if delim_ind <= 0:
            return ""
        else:
            return self.current_command[:delim_ind]

    @property
    def comp(self):
        if self.command_type != "C_COMMAND":
            raise Exception("Incorrect Type")

        delim_ind1 = self.current_command.find("=")
        delim_ind2 = self.current_command.find(";")

        # Exception of both jump and dest exist
        if delim_ind1 == -1 and delim_ind2 >= 0:
            return self.current_command[:delim_ind2]
        elif delim_ind1 >= 0 and delim_ind2 == -1:
            return self.current_command[delim_ind1+1:]
        else:
            raise Exception("Line {}: Invalid Command [{}]".format(
                self.command_stream.tell(),
                self.current_command))

    @property
    def jump(self):
        if self.command_type != "C_COMMAND":
            raise Exception("Incorrect Type")

        delim_ind = self.current_command.find(";")
        if delim_ind == -1:
            return ""
        else:
            return self.current_command[delim_ind + 1:]

    @property
    def has_more_commands(self):
        file_curr_line = self.command_stream.tell()

        while True:

            peek_next = self.command_stream.readline()

            peek_next = self.__remove_comments(peek_next)

            if peek_next.isspace():
                continue
            elif peek_next == "":
                self.command_stream.seek(file_curr_line)
                return False
            else:
                self.command_stream.seek(file_curr_line)
                return True

    def advance(self):
        """
        Sets current_command to the next command. Immediately returns if no
        more commands left.
        """
        if not self.has_more_commands:
            return

        while True:
            temp_cmd = self.command_stream.readline()

            temp_cmd = self.__remove_comments(temp_cmd)

            if not temp_cmd.isspace():
                break

        self.current_command = temp_cmd.strip("\t\n ")
        return

    def __remove_comments(self, cmd):
        temp_cmd = cmd
        for i in range(len(cmd) - 1):
            if temp_cmd[i] == "/" and temp_cmd[i + 1] == "/":
                temp_cmd = temp_cmd[:i]
                break
        return temp_cmd


if __name__ == "__main__":
    parse = Parser("empty.txt")

    parse.current_command = "@"
    print(parse.current_command)
    print(parse.command_type())
