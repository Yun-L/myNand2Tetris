__author__ = "Yun-L"


class Parser:
    """Breaks each assembly command into its underlying fields and symbols"""

    def __init__(self, filename):

        self.command_stream = open(filename, "r")
        self.current_command = None
        self.has_more_commands = True

    def advance(self):

        if not self.has_more_commands:
            return

        self.current_command = self.command_stream.readline()

        if self.current_command == "":
            self.has_more_commands = False

        return

    def command_type(self):
        """Returns string 'A_COMMAND' | 'C_COMMAND' | 'L_COMMAND'"""
        return "TODO"

    def symbol(self):
        return "TODO"

    def dest(self):
        return "TODO"

    def comp(self):
        return "TODO"

    def jump(self):
        return "TODO"
