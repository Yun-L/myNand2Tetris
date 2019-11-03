__author__ = "Yun-L"

import unittest

from code import Code

class TestCode(unittest.TestCase):

    def setUp(self):
        self.code = Code("", "", "0")
    
    def test_dest(self):
        self.code.dest = ""
        self.assertEqual(self.code.dest, "000")

        self.code.dest = "M"
        self.assertEqual(self.code.dest, "001")

        self.code.dest = "D"
        self.assertEqual(self.code.dest, "010")

        self.code.dest = "MD"
        self.assertEqual(self.code.dest, "011")

        self.code.dest = "A"
        self.assertEqual(self.code.dest, "100")

        self.code.dest = "AM"
        self.assertEqual(self.code.dest, "101")

        self.code.dest = "AD"
        self.assertEqual(self.code.dest, "110")

        self.code.dest = "AMD"
        self.assertEqual(self.code.dest, "111")

        
    def test_jump(self):
        self.code.jump = ""
        self.assertEqual(self.code.jump, "000")

        self.code.jump = "JGT"
        self.assertEqual(self.code.jump, "001")

        self.code.jump = "JEQ"
        self.assertEqual(self.code.jump, "010")

        self.code.jump = "JGE"
        self.assertEqual(self.code.jump, "011")

        self.code.jump = "JLT"
        self.assertEqual(self.code.jump, "100")

        self.code.jump = "JNE"
        self.assertEqual(self.code.jump, "101")

        self.code.jump = "JLE"
        self.assertEqual(self.code.jump, "110")

        self.code.jump = "JMP"
        self.assertEqual(self.code.jump, "111")

    
    def test_comp_len_1(self):
        self.code.comp = "0"
        self.assertEqual(self.code.comp, "0101010")

        self.code.comp = "1"
        self.assertEqual(self.code.comp, "0111111")

        self.code.comp = "D"
        self.assertEqual(self.code.comp, "0001100")

        self.code.comp = "A"
        self.assertEqual(self.code.comp, "0110000")

        self.code.comp = "M"
        self.assertEqual(self.code.comp, "1110000")


    def test_comp_len_2(self):
        self.code.comp = "-1"
        self.assertEqual(self.code.comp, "0111010")

        self.code.comp = "!D"
        self.assertEqual(self.code.comp, "0001101")

        self.code.comp = "!A"
        self.assertEqual(self.code.comp, "0110001")

        self.code.comp = "!M"
        self.assertEqual(self.code.comp, "1110001")

        self.code.comp = "-D"
        self.assertEqual(self.code.comp, "0001111")

        self.code.comp = "-A"
        self.assertEqual(self.code.comp, "0110011")

        self.code.comp = "-M"
        self.assertEqual(self.code.comp, "1110011")


    def test_comp_len_3(self):
        self.code.comp = "D+1"
        self.assertEqual(self.code.comp, "0011111")

        self.code.comp = "A+1"
        self.assertEqual(self.code.comp, "0110111")

        self.code.comp = "M+1"
        self.assertEqual(self.code.comp, "1110111")

        self.code.comp = "D-1"
        self.assertEqual(self.code.comp, "0001110")

        self.code.comp = "A-1"
        self.assertEqual(self.code.comp, "0110010")

        self.code.comp = "M-1"
        self.assertEqual(self.code.comp, "1110010")

        self.code.comp = "D+A"
        self.assertEqual(self.code.comp, "0000010")

        self.code.comp = "D+M"
        self.assertEqual(self.code.comp, "1000010")

        self.code.comp = "D-A"
        self.assertEqual(self.code.comp, "0010011")

        self.code.comp = "D-M"
        self.assertEqual(self.code.comp, "1010011")

        self.code.comp = "D&A"
        self.assertEqual(self.code.comp, "0000000")

        self.code.comp = "D&M"
        self.assertEqual(self.code.comp, "1000000")

        self.code.comp = "D|A"
        self.assertEqual(self.code.comp, "0010101")

        self.code.comp = "D|M"
        self.assertEqual(self.code.comp, "1010101")

    def test_invalid(self):
        # Invalid dest but should return as if empty
        self.code.dest = "123456"
        self.assertEqual(self.code.dest, "000")

        with self.assertRaises(Exception):
            self.code.jump = None

        with self.assertRaises(Exception):
            self.code.jump = "AOEUAOEU"

        with self.assertRaises(Exception):
            self.code.comp = "AOEU"

        with self.assertRaises(Exception):
            self.code.comp = "H"

        with self.assertRaises(Exception):
            self.code.comp = "HH"

        with self.assertRaises(Exception):
            self.code.comp = "HHH"

        with self.assertRaises(Exception):
            self.code.comp = None

if __name__ == "__main__":
    unittest.main()
