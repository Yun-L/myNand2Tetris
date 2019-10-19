__author__ = "Yun-L"

import unittest

from parser import *


class TestParser(unittest.TestCase):

    def test_command_type(self):
        self.parse = Parser("empty.txt")

        self.parse.current_command = "@"
        print(self.parse.current_command)
        print(self.parse.command_type())

        '''
        self.assertEqual(self.parse.command_type(), "A_COMMAND")

        self.parser.current_command = "  \t@1auoe651651"
        self.assertEqual(self.parse.command_type(), "A_COMMAND")
        '''


if __name__ == '__main__':
    unittest.main()
