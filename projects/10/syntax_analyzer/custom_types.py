from enum import Enum, auto


class TokenType(Enum):
    """Details different token types"""

    KEYWORD = auto()
    SYMBOL = auto()
    IDENTIFIER = auto()
    INT_CONST = auto()
    STRING_CONST = auto()


TokenType.keywords = ["class",
                      "constructor",
                      "function",
                      "method",
                      "field",
                      "static",
                      "var",
                      "int",
                      "char",
                      "boolean",
                      "void",
                      "true",
                      "false",
                      "null",
                      "this",
                      "let",
                      "do",
                      "if",
                      "else",
                      "while",
                      "return"]

TokenType.symbols = ["{",
                     "}",
                     "(",
                     ")",
                     "[",
                     "]",
                     ".",
                     ",",
                     ";",
                     "+",
                     "-",
                     "*",
                     "/",
                     "&",
                     "|",
                     "<",
                     ">",
                     "=",
                     "~"]


class KeyWordType(str, Enum):
    """Details different key-word types"""

    CLASS = "class"
    METHOD = "method"
    FUNCTION = "function"
    CONSTRUCTOR = "constructor"
    INT = "int"
    BOOLEAN = "boolean"
    CHAR = "char"
    VOID = "void"
    VAR = "var"
    STATIC = "static"
    FIELD = "field"
    LET = "let"
    DO = "do"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    RETURN = "return"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    THIS = "this"


def keyword_map(token: str,
                mapping={"class": KeyWordType.CLASS,
                         "constructor": KeyWordType.CONSTRUCTOR,
                         "function": KeyWordType.FUNCTION,
                         "method": KeyWordType.METHOD,
                         "field": KeyWordType.FIELD,
                         "static": KeyWordType.STATIC,
                         "var": KeyWordType.VAR,
                         "int": KeyWordType.INT,
                         "char": KeyWordType.CHAR,
                         "boolean": KeyWordType.BOOLEAN,
                         "void": KeyWordType.VOID,
                         "true": KeyWordType.TRUE,
                         "false": KeyWordType.FALSE,
                         "null": KeyWordType.NULL,
                         "this": KeyWordType.THIS,
                         "let": KeyWordType.LET,
                         "do": KeyWordType.DO,
                         "if": KeyWordType.IF,
                         "else": KeyWordType.ELSE,
                         "while": KeyWordType.WHILE,
                         "return": KeyWordType.RETURN}):
    try:
        return mapping[token]
    except Exception as e:
        raise(f"'{token}' has no KeyWordType. {e}")
