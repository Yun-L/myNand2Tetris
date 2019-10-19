__author__ = "Yun-L"


class Parser:
    """Breaks each assembly command into its underlying fields and symbols"""

    def __init__(self, filename):

        self.command_stream = open(filename, "r")
        self.current_command = None

    def __del__(self):
        self.command_stream.close()

    def command_type(self):
        """Returns string 'A_COMMAND' | 'C_COMMAND' | 'L_COMMAND'"""
        if self.current_command[0] == "@":
            return "A_COMMAND"
        elif self.current_command[0] == "(":
            return "L_COMMAND"
        else:
            return "C_COMMAND"

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
        if delim_ind1 == -1 and delim_ind2 >= 0:
            return self.current_command[:delim_ind2]
        elif delim_ind1 >= 0 and delim_ind2 == -1:
            return self.current_command[delim_ind1+1:]
        else:
            raise Exception("Line {}: Invalid Command [{}]".format(
                self.current_command.tell(),
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
        if self.current_command == "":
            return False
        else:
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

            if temp_cmd == "":  # file objects return "" at EOF
                break

            temp_cmd = self.__remove_comments(temp_cmd)
            temp_cmd = temp_cmd.strip("\t ")
            if temp_cmd.isspace():
                continue
            else:
                break

        self.current_command = temp_cmd
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
