__author__ = "Yun-L"

import unittest

from parser import Parser


class TestParser(unittest.TestCase):

    def test_comments(self):
        self.parse = Parser("test_comments.asm")
        self.assertEqual(self.parse.current_command, None)
        self.assertEqual(self.parse.has_more_commands, False)

    def test_C_commands(self):
        self.parse = Parser("test_C_commands.asm")

        # A=D
        self.parse.advance()
        self.assertEqual(self.parse.command_type, "C_COMMAND")
        self.assertEqual(self.parse.dest, "A")
        self.assertEqual(self.parse.comp, "D")
        self.assertEqual(self.parse.jump, "")

        # D=A
        self.parse.advance()
        self.assertEqual(self.parse.command_type, "C_COMMAND")
        self.assertEqual(self.parse.dest, "D")
        self.assertEqual(self.parse.comp, "A")
        self.assertEqual(self.parse.jump, "")

        # M=M-D
        self.parse.advance()
        self.assertEqual(self.parse.command_type, "C_COMMAND")
        self.assertEqual(self.parse.dest, "M")
        self.assertEqual(self.parse.comp, "M-D")
        self.assertEqual(self.parse.jump, "")

        # M=M
        self.parse.advance()
        self.assertEqual(self.parse.command_type, "C_COMMAND")
        self.assertEqual(self.parse.dest, "M")
        self.assertEqual(self.parse.comp, "M")
        self.assertEqual(self.parse.jump, "")

        # 0;LOOP
        self.parse.advance()
        self.assertEqual(self.parse.command_type, "C_COMMAND")
        self.assertEqual(self.parse.dest, "")
        self.assertEqual(self.parse.comp, "0")
        self.assertEqual(self.parse.jump, "LOOP")

        # D;HH
        self.parse.advance()
        self.assertEqual(self.parse.command_type, "C_COMMAND")
        self.assertEqual(self.parse.dest, "")
        self.assertEqual(self.parse.comp, "D")
        self.assertEqual(self.parse.jump, "HH")

        # M;AOEU
        self.parse.advance()
        self.assertEqual(self.parse.command_type, "C_COMMAND")
        self.assertEqual(self.parse.dest, "")
        self.assertEqual(self.parse.comp, "M")
        self.assertEqual(self.parse.jump, "AOEU")

        # check EOF
        self.assertEqual(self.parse.has_more_commands, False)
        self.parse.advance()
        self.assertEqual(self.parse.has_more_commands, False)

    def test_A_commands(self):
        self.parse = Parser("test_A_commands.asm")

        # @5
        self.parse.advance()
        self.assertEqual(self.parse.command_type, "A_COMMAND")
        self.assertEqual(self.parse.symbol, "5")


"""
    def test_L_commands(self):
        self.parse = Parser("test_L_commands")
"""


if __name__ == '__main__':
    unittest.main()
