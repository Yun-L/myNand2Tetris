import unittest
from jack_tokenizer import JackTokenizer
from custom_types import TokenType, KeyWordType


class TestTokenizer(unittest.TestCase):

    def test_has_more_tokens(self):
        # file with only comments
        with open("test_files/empty.jack", "r") as infile:
            t = JackTokenizer(infile)
            self.assertEqual(t.has_more_tokens(), False)

        # file with arbitrary text
        with open("test_files/nonempty.jack", "r") as infile:
            t = JackTokenizer(infile)
            self.assertEqual(t.has_more_tokens(), True)

        return

    def test_advance(self):
        # file with only comments
        with open("test_files/empty.jack", "r") as infile:
            t = JackTokenizer(infile)
            t.advance()
            self.assertEqual(t.curr_token, None)

        # file with arbitrary text
        with open("test_files/nonempty.jack", "r") as infile:
            t = JackTokenizer(infile)
            t.advance()
            self.assertEqual(t.curr_token, "constructor")
            t.advance()
            self.assertEqual(t.curr_token, "function")
            t.advance()
            self.assertEqual(t.curr_token, "{")
            t.advance()
            self.assertEqual(t.curr_token, "}")
            t.advance()
            self.assertEqual(t.curr_token, "165")
            t.advance()
            self.assertEqual(t.curr_token, '"ao{eu"')
            t.advance()
            self.assertEqual(t.curr_token, "{")
            t.advance()
            self.assertEqual(t.curr_token, "hhh")
            t.advance()
            self.assertEqual(t.curr_token, '""')
            t.advance()
            self.assertEqual(t.curr_token, "_aaa555")
            t.advance()
            self.assertEqual(t.curr_token, "_aaa555")

    def test_token_type(self):
        with open("test_files/nonempty.jack", "r") as infile:
            t = JackTokenizer(infile)
            t.advance()  # constructor
            self.assertEqual(t.token_type(), TokenType.KEYWORD)
            t.advance()  # function
            self.assertEqual(t.token_type(), TokenType.KEYWORD)
            t.advance()  # {
            self.assertEqual(t.token_type(), TokenType.SYMBOL)
            t.advance()  # }
            self.assertEqual(t.token_type(), TokenType.SYMBOL)
            t.advance()  # 165
            self.assertEqual(t.token_type(), TokenType.INT_CONST)
            t.advance()  # "ao{eu"
            self.assertEqual(t.token_type(), TokenType.STRING_CONST)
            t.advance()  # {
            self.assertEqual(t.token_type(), TokenType.SYMBOL)
            t.advance()  # hhh
            self.assertEqual(t.token_type(), TokenType.IDENTIFIER)
            t.advance()  # ""
            self.assertEqual(t.token_type(), TokenType.STRING_CONST)
            t.advance()  # _aaa555
            self.assertEqual(t.token_type(), TokenType.IDENTIFIER)
            t.advance()  # _aaa555
            self.assertEqual(t.token_type(), TokenType.IDENTIFIER)
            return

    def test_token_return_funcs(self):
        with open("test_files/nonempty.jack", "r") as infile:
            t = JackTokenizer(infile)
            t.advance()  # constructor
            self.assertEqual(t.key_word(), KeyWordType.CONSTRUCTOR)
            t.advance()  # function
            self.assertEqual(t.key_word(), KeyWordType.FUNCTION)
            t.advance()  # {
            self.assertEqual(t.symbol(), "{")
            t.advance()  # }
            self.assertEqual(t.symbol(), "}")
            t.advance()  # 165
            self.assertEqual(t.int_val(), 165)
            t.advance()  # "ao{eu"
            self.assertEqual(t.string_val(), "ao{eu")
            t.advance()  # {
            self.assertEqual(t.symbol(), "{")
            t.advance()  # hhh
            self.assertEqual(t.identifier(), "hhh")
            t.advance()  # ""
            self.assertEqual(t.string_val(), "")
            t.advance()  # _aaa555
            self.assertEqual(t.identifier(), "_aaa555")
            t.advance()  # _aaa555
            self.assertEqual(t.identifier(), "_aaa555")
            return


if __name__ == "__main__":
    unittest.main()
