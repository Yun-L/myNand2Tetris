from custom_types import TokenType, KeyWordType, keyword_map


class JackTokenizer(object):
    """Removes all comments and white space from the input stream and breaks
    it into Jack-language tokens."""

    def __init__(self, input_file_stream):
        self.__file_stream = input_file_stream
        self.__curr_token = None

    @property
    def curr_token(self):
        return self.__curr_token

    def __handle_comment(self):
        """Only call this if a "/", signifying the start of a comment, is
        found. Exhausts the comment that input_file_stream is currently on."""
        c = self.__file_stream.read(1)
        if c == "/":
            # line comment
            self.__file_stream.readline()
        elif c == "*":
            # block comment
            comment_end = False
            while True:
                c = self.__file_stream.read(1)

                if c == "":
                    break

                if c == "/" and comment_end:
                    break
                else:
                    comment_end = False

                if c == "*":
                    comment_end = True

            if not comment_end:
                raise Exception("No end of block comment found")
        else:
            raise Exception("Not a comment")

        return

    def has_more_tokens(self) -> bool:
        """Returns true if there are any more tokens in the file"""
        file_curr_pos = self.__file_stream.tell()
        skip_chars = ["\t", "\n", " "]
        status = False
        while True:
            curr_char = self.__file_stream.read(1)
            if curr_char == "/":
                pos = self.__file_stream.tell()
                temp = self.__file_stream.read(1)
                self.__file_stream.seek(pos)
                if temp == "/" or temp == "*":
                    self.__handle_comment()
                else:
                    status = True
                    self.__file_stream.seek(file_curr_pos)
                    break
            elif curr_char in skip_chars:
                continue
            elif curr_char == "":
                break
            else:
                status = True
                self.__file_stream.seek(file_curr_pos)
                break
        return status

    def advance(self) -> None:
        """Gets next token from the input and makes it the current token. Should
        only be called if has_more_tokens is true."""
        if self.has_more_tokens():
            skip_chars = ["\t", "\n", " "]
            token_chars = []

            curr_char = self.__file_stream.read(1)
            while True:
                # skip whitespace
                if curr_char == "":
                    return
                elif curr_char in skip_chars:
                    curr_char = self.__file_stream.read(1)
                elif curr_char == "/":
                    pos = self.__file_stream.tell()
                    temp = self.__file_stream.read(1)
                    self.__file_stream.seek(pos)
                    if temp != "/" and temp != "*":
                        token_chars += curr_char
                        break
                    self.__handle_comment()
                    curr_char = self.__file_stream.read(1)
                else:
                    token_chars += curr_char
                    break

            if curr_char in TokenType.symbols:
                # if token is a symbol
                pass
            elif curr_char == '"':
                # if token looks to be a string constant
                while True:
                    curr_char = self.__file_stream.read(1)
                    if curr_char == '"':
                        token_chars += curr_char
                        break
                    elif curr_char == "\n":
                        raise Exception(
                            "newline char found in string constant")
                    elif curr_char == "":
                        raise Exception("string constant has no end")
                    else:
                        token_chars += curr_char
            else:
                # if token looks to be a keyword, int constant or identifier
                while True:
                    retpos = self.__file_stream.tell()
                    curr_char = self.__file_stream.read(1)
                    if curr_char in skip_chars or curr_char in TokenType.symbols:
                        self.__file_stream.seek(retpos)
                        break
                    elif curr_char == "":
                        break
                    else:
                        token_chars += curr_char

            self.__curr_token = "".join(token_chars)
        return

    def token_type(self) -> TokenType:
        """Returns the type of the current token"""
        def is_string_const(token: str) -> bool:
            if len(token) < 2:
                return False

            if token[0] != '"' or token[-1] != '"':
                return False

            if token.find("\n") != -1:
                return False

            return True

        def is_integer_const(token: str) -> bool:
            try:
                val = int(token)
            except ValueError:
                return False

            if val < 0 or val > 32767:
                return False

            return True

        def is_identifier(token: str) -> bool:
            if not (token[0].isalpha() or token[0] == "_"):
                return False

            for i in range(2, len(token)):
                if not (token[i].isalnum() or token[i] == "_"):
                    return False

            return True
        if self.__curr_token in TokenType.keywords:
            return TokenType.KEYWORD
        elif self.__curr_token in TokenType.symbols:
            return TokenType.SYMBOL
        elif is_string_const(self.__curr_token):
            return TokenType.STRING_CONST
        elif is_integer_const(self.__curr_token):
            return TokenType.INT_CONST
        elif is_identifier(self.__curr_token):
            return TokenType.IDENTIFIER
        else:
            raise Exception(f"invalid token '{self.__curr_token}'")
        return

    def key_word(self) -> KeyWordType:
        """Returns the keyword which is the current token. Should only be called when
        the current token type is KEYWORD"""
        if self.token_type() != TokenType.KEYWORD:
            raise Exception(f"{self.token_type()} is not KEYWORD")
        return keyword_map(self.__curr_token)

    def symbol(self) -> str:
        """Returns the 'character' which is the current token. Should only be
        called when the current token type is SYMBOL"""
        if self.token_type() != TokenType.SYMBOL:
            raise Exception(f"{self.token_type()} is not SYMBOL")
        return self.__curr_token

    def identifier(self) -> str:
        """Returns the identifier which is the current token. Should only be
        called when the current token type is IDENTIFIER"""
        if self.token_type() != TokenType.IDENTIFIER:
            raise Exception(f"{self.token_type()} is not IDENTIFIER")
        return self.__curr_token

    def int_val(self) -> int:
        """Returns the integer value of the current token. Should only be called when
        the current token type is INT_CONST"""
        if self.token_type() != TokenType.INT_CONST:
            raise Exception(f"{self.token_type()} is not INT_CONST")
        return int(self.__curr_token)

    def string_val(self) -> str:
        """Returns the string value of the current token, with no double quotes.
        Should only be called when the current token type is STRING_CONST"""
        if self.token_type() != TokenType.STRING_CONST:
            raise Exception(f"{self.token_type()} is not STRING_CONST")
        return self.__curr_token.strip('"')
