from jack_tokenizer import JackTokenizer
from custom_types import KeyWordType, TokenType


class CompilationEngine():
    """Recursive top-down parser"""

    def __init__(self, token_stream: JackTokenizer, output_file_stream,
                 ind_amount=2):
        self.__token_stream = token_stream
        self.__outfile = output_file_stream
        self.__ind_amount = ind_amount  # how many spaces for an indent
        self.__ind_level = 0
        return

    def __tag(self, tag_name: str, ind_level=None, end=False, newline=True):
        """ Writes to the output file a tag of form <tag_name>.
        'ind_level' represents how many times the tag will be indented.
        'end' signals to include a '/' to write an ending tag: </tag_name>
        'newline' signals to include a newline after the tag: <tag_name>\n
        """
        if ind_level is None:
            ind_level = self.__ind_level

        tag = []
        tag += [" "*(self.__ind_amount * ind_level) + "<"]
        if end:
            tag += ["/"]
        tag += [f"{tag_name}>"]
        if newline:
            tag += ["\n"]
        self.__outfile.write("".join(tag))
        return

    def __term(self, tag_name, content):
        """ Helper function to write a terminal """
        self.__tag(tag_name, newline=False)
        self.__outfile.write(f" {content} ")
        self.__tag(tag_name, 0, end=True)

    def __w_keyword(self, comp: KeyWordType) -> bool:
        val = self.__token_stream.key_word()
        if val != comp:
            return False
        self.__term("keyword", val.value)
        return True

    def __w_symbol(self, comp: str) -> bool:
        val = self.__token_stream.symbol()
        if val != comp:
            return False
        self.__term("symbol", val)
        return True

    def __w_identifier(self):
        val = self.__token_stream.identifier()
        self.__term("identifier", val)
        return

    def __w_int(self):
        val = self.__token_stream.int_val()
        self.__term("integerConstant", val)
        return

    def __w_str(self):
        val = self.__token_stream.string_val()
        self.__term("stringConstant", val)
        return

    def compile_class(self) -> True:
        self.__tag("class")
        self.__ind_level += 1
        self.__token_stream.advance()
        self.__w_keyword(KeyWordType.CLASS)
        # className
        self.__token_stream.advance()
        self.__w_identifier()
        self.__token_stream.advance()
        self.__w_symbol("{")
        self.__token_stream.advance()
        while self.compile_class_var_dec():
            self.__token_stream.advance()
        while self.compile_subroutine():
            self.__token_stream.advance()
        self.__w_symbol("}")
        self.__ind_level -= 1
        self.__tag("class", end=True)
        self.__token_stream.advance()
        return True

    def compile_class_var_dec(self) -> True:
        """ classVarDec => ('static' | 'field') type varName (',' varName)* ';'
        Returns False if first token is invalid, True otherwise. """
        if self.__token_stream.token_type() != TokenType.KEYWORD:
            return False

        val = self.__token_stream.key_word()
        if val != KeyWordType.STATIC and val != KeyWordType.FIELD:
            return False

        self.__tag("classVarDec")
        self.__ind_level += 1

        # static | field
        self.__w_keyword(val)

        # type
        self.__token_stream.advance()
        if self.__token_stream.token_type() == TokenType.KEYWORD:
            accept_lst = [KeyWordType.INT,
                          KeyWordType.CHAR,
                          KeyWordType.BOOLEAN]

            val = self.__token_stream.key_word()
            if val not in accept_lst:
                raise Exception(f"'{val}' not a valid keyword for 'type'")
            self.__w_keyword(val)
        else:
            # className if not int | char | boolean
            self.__w_identifier()

        # varName
        self.__token_stream.advance()
        self.__w_identifier()

        # (',' varName)*
        self.__token_stream.advance()
        while self.__token_stream.symbol() == ",":
            self.__w_symbol(",")
            self.__token_stream.advance()
            self.__w_identifier()
            self.__token_stream.advance()

        # ;
        self.__w_symbol(";")

        # close off classVarDec
        self.__ind_level -= 1
        self.__tag("classVarDec", end=True)
        return True

    def compile_subroutine(self) -> True:
        """ subroutineDec => ('constructor' | 'function' | 'method')
        ( 'void' | type) subroutineName '(' parameterList ')' subroutineBody
        Returns False if first token is invalid, True otherwise."""

        if self.__token_stream.token_type() != TokenType.KEYWORD:
            return False

        accept_lst = [KeyWordType.CONSTRUCTOR,
                      KeyWordType.FUNCTION,
                      KeyWordType.METHOD]
        val = self.__token_stream.key_word()
        if val not in accept_lst:
            return False

        self.__tag("subroutineDec")
        self.__ind_level += 1

        # 'constructor' | 'function' | 'method'
        self.__w_keyword(val)

        # 'void' | type => ('int' | 'char' | 'boolean' | className)
        self.__token_stream.advance()
        if self.__token_stream.token_type() == TokenType.KEYWORD:
            accept_lst = [KeyWordType.INT,
                          KeyWordType.CHAR,
                          KeyWordType.BOOLEAN,
                          KeyWordType.VOID]

            val = self.__token_stream.key_word()
            if val not in accept_lst:
                raise Exception(
                    f"'{val}' not a valid keyword for 'void' or 'type'")
            self.__w_keyword(val)
        else:
            # className
            self.__w_identifier()

        # subroutineName
        self.__token_stream.advance()
        self.__w_identifier()

        # '('
        self.__token_stream.advance()
        self.__w_symbol("(")

        # parameterList
        self.__token_stream.advance()
        if not self.compile_parameter_list():
            self.__token_stream.advance()

        # ')'
        self.__w_symbol(")")

        # subroutineBody
        self.__tag("subroutineBody")
        self.__ind_level += 1

        # '{'
        self.__token_stream.advance()
        self.__w_symbol("{")

        # varDec*
        self.__token_stream.advance()
        while self.compile_var_dec():
            self.__token_stream.advance()

        # statements
        if not self.compile_statements():
            self.__token_stream.advance()

        # '}'
        self.__w_symbol("}")

        # close off subroutineBody
        self.__ind_level -= 1
        self.__tag("subroutineBody", end=True)

        # close off subroutineDec
        self.__ind_level -= 1
        self.__tag("subroutineDec", end=True)

        return True

    def compile_parameter_list(self) -> bool:
        """ parameterList => ((type varName) (',' type varName)*)?
        returns True if trailing advance() called on the token stream.
        returns False otherwise"""
        self.__tag("parameterList")
        self.__ind_level += 1

        tok_type = self.__token_stream.token_type()
        # check if first token is 'type'
        if tok_type == TokenType.KEYWORD:
            accept_lst = [KeyWordType.INT,
                          KeyWordType.CHAR,
                          KeyWordType.BOOLEAN]

            val = self.__token_stream.key_word()
            if val not in accept_lst:
                raise Exception(f"'{val}' not a valid keyword for 'type'")
            self.__w_keyword(val)
        elif tok_type == TokenType.IDENTIFIER:
            # className if not int | char | boolean
            self.__w_identifier()
        else:
            self.__ind_level -= 1
            self.__tag("parameterList", end=True)
            # trailing advance from before the function call
            return True

        # varName
        self.__token_stream.advance()
        self.__w_identifier()

        # (',' type varName)*
        self.__token_stream.advance()
        while self.__token_stream.symbol() == ",":
            self.__w_symbol(",")
            self.__token_stream.advance()
            if self.__token_stream.token_type() == TokenType.KEYWORD:
                accept_lst = [KeyWordType.INT,
                              KeyWordType.CHAR,
                              KeyWordType.BOOLEAN]

                val = self.__token_stream.key_word()
                if val not in accept_lst:
                    raise Exception(f"'{val}' not a valid keyword for 'type'")
                self.__w_keyword(val)
            else:
                self.__w_identifier()

            self.__token_stream.advance()
            self.__w_identifier()
            self.__token_stream.advance()

        # close off parameterList
        self.__ind_level -= 1
        self.__tag("parameterList", end=True)
        return True

    def compile_var_dec(self):
        """ varDec => 'var' type varName (',' varName)* ';'
        Returns True if successful
        Returns False if first token is invalid for varDec"""
        if self.__token_stream.token_type() != TokenType.KEYWORD:
            return False

        if self.__token_stream.key_word() != KeyWordType.VAR:
            return False

        self.__tag("varDec")
        self.__ind_level += 1

        # 'var'
        self.__w_keyword(KeyWordType.VAR)

        # type
        self.__token_stream.advance()
        if self.__token_stream.token_type() == TokenType.KEYWORD:
            accept_lst = [KeyWordType.INT,
                          KeyWordType.CHAR,
                          KeyWordType.BOOLEAN]

            val = self.__token_stream.key_word()
            if val not in accept_lst:
                raise Exception(f"'{val}' not a valid keyword for 'type'")
            self.__w_keyword(val)
        else:
            self.__w_identifier()

        # varName
        self.__token_stream.advance()
        self.__w_identifier()

        # (',' varName)*
        self.__token_stream.advance()
        while self.__token_stream.symbol() == ",":
            self.__w_symbol(",")
            self.__token_stream.advance()
            self.__w_identifier()
            self.__token_stream.advance()

        # ';'
        self.__w_symbol(";")

        # close off varDec
        self.__ind_level -= 1
        self.__tag("varDec", end=True)

        return True

    def compile_statements(self) -> bool:
        """ statements => statement*
        statement => letStatement | ifStatement | whileStatement | doStatement
        | returnStatement"""
        def is_statement():
            """Returns true if the current token is valid for statement"""
            if self.__token_stream.token_type() != TokenType.KEYWORD:
                return False

            accept_lst = [KeyWordType.LET,
                          KeyWordType.IF,
                          KeyWordType.WHILE,
                          KeyWordType.DO,
                          KeyWordType.RETURN]

            val = self.__token_stream.key_word()
            if val not in accept_lst:
                return False
            return True

        self.__tag("statements")
        self.__ind_level += 1

        while is_statement():
            val = self.__token_stream.key_word()
            trailing_adv = False
            if val == KeyWordType.LET:
                trailing_adv = self.compile_let()
            elif val == KeyWordType.IF:
                trailing_adv = self.compile_if()
            elif val == KeyWordType.WHILE:
                trailing_adv = self.compile_while()
            elif val == KeyWordType.DO:
                trailing_adv = self.compile_do()
            elif val == KeyWordType.RETURN:
                trailing_adv = self.compile_return()
            else:
                raise Exception(f"{val} is not a valid starting keyword for"
                                "any statement.")

            if not trailing_adv:
                self.__token_stream.advance()

        # close off statements
        self.__ind_level -= 1
        self.__tag("statements", end=True)
        return True

    def compile_if(self):
        """ ifStatement => 'if' '(' expression ')' '{' statements '}' ('else'
        '{' statements '}')?"""
        self.__tag("ifStatement")
        self.__ind_level += 1

        # 'if'
        self.__w_keyword(KeyWordType.IF)

        # '('
        self.__token_stream.advance()
        self.__w_symbol("(")

        # expression
        self.__token_stream.advance()
        if not self.compile_expression():
            self.__token_stream.advance()

        # ')'
        self.__w_symbol(")")

        # '{'
        self.__token_stream.advance()
        self.__w_symbol("{")

        # statements
        self.__token_stream.advance()
        if not self.compile_statements():
            self.__token_stream.advance()

        # '}'
        self.__w_symbol("}")

        # ('else' '{' statements '}')?
        self.__token_stream.advance()
        if (self.__token_stream.token_type() == TokenType.KEYWORD
                and self.__token_stream.key_word() == KeyWordType.ELSE):
            self.__w_keyword(KeyWordType.ELSE)
            self.__token_stream.advance()
            self.__w_symbol("{")
            self.__token_stream.advance()
            if not self.compile_statements():
                self.__token_stream.advance()
            self.__w_symbol("}")
            trailing_adv = False
        else:
            trailing_adv = True

        self.__ind_level -= 1
        self.__tag("ifStatement", end=True)
        return trailing_adv

    def compile_let(self) -> bool:
        """ letStatement => 'let' varName ('[' expression ']')? '=' expression ';'
        returns True if there was a trailing token stream advance
        """
        self.__tag("letStatement")
        self.__ind_level += 1

        # 'let'
        self.__w_keyword(KeyWordType.LET)

        # varName
        self.__token_stream.advance()
        self.__w_identifier()

        # ('[' expression ']')?
        self.__token_stream.advance()
        if self.__token_stream.symbol() == "[":
            self.__w_symbol("[")
            self.__token_stream.advance()
            if not self.compile_expression():
                self.__token_stream.advance()
            self.__w_symbol("]")
            self.__token_stream.advance()

        # "="
        self.__w_symbol("=")

        # expression
        self.__token_stream.advance()
        if not self.compile_expression():
            self.__token_stream.advance()

        # ";"
        self.__w_symbol(";")

        self.__ind_level -= 1
        self.__tag("letStatement", end=True)
        return False

    def compile_while(self) -> bool:
        """ whileStatement => 'while' '(' expression ')' '{' statements '}'
        returns True if there was a trailing token stream advance"""
        self.__tag("whileStatement")
        self.__ind_level += 1

        # 'while'
        self.__w_keyword(KeyWordType.WHILE)

        # '('
        self.__token_stream.advance()
        self.__w_symbol("(")

        # expression
        self.__token_stream.advance()
        if not self.compile_expression():
            self.__token_stream.advance()

        # ')'
        self.__w_symbol(")")

        # '{'
        self.__token_stream.advance()
        self.__w_symbol("{")

        # statements
        self.__token_stream.advance()
        if not self.compile_statements():
            self.__token_stream.advance()

        # '}'
        self.__w_symbol("}")

        self.__ind_level -= 1
        self.__tag("whileStatement", end=True)
        return False

    def compile_do(self) -> bool:
        """ doStatement => 'do' subroutineCall ';'
        returns True if there was a trailing token stream advance"""
        self.__tag("doStatement")
        self.__ind_level += 1

        # 'do'
        self.__w_keyword(KeyWordType.DO)

        # subroutineCall
        self.__token_stream.advance()
        self.__w_identifier()

        self.__token_stream.advance()
        curr_sym = self.__token_stream.symbol()
        if curr_sym == "(":
            self.__w_symbol("(")
            self.__token_stream.advance()
            if not self.compile_expression_list():
                self.__token_stream.advance()
            self.__w_symbol(")")
        elif curr_sym == ".":
            self.__w_symbol(".")
            self.__token_stream.advance()
            self.__w_identifier()
            self.__token_stream.advance()
            self.__w_symbol("(")
            self.__token_stream.advance()
            if not self.compile_expression_list():
                self.__token_stream.advance()
            self.__w_symbol(")")
        else:
            raise Exception(f"Invalid symbol '{curr_sym}'")

        self.__token_stream.advance()
        self.__w_symbol(";")

        self.__ind_level -= 1
        self.__tag("doStatement", end=True)
        return False

    def compile_return(self) -> bool:
        """ returnStatement => 'return' expression? ';'
        returns True if there was a trailing token stream advance"""
        self.__tag("returnStatement")
        self.__ind_level += 1

        # 'return'
        self.__w_keyword(KeyWordType.RETURN)

        # expression?
        self.__token_stream.advance()
        if (self.__token_stream.token_type() != TokenType.SYMBOL
                or self.__token_stream.symbol() != ";"):
            if not self.compile_expression():
                self.__token_stream.advance()

        # ";"
        self.__w_symbol(";")

        # close off returnStatement
        self.__ind_level -= 1
        self.__tag("returnStatement", end=True)
        return False

    def compile_expression(self) -> bool:
        """ expression => term (op term)*
        returns True if there was a trailing token stream advance"""
        def is_op():
            valid_op = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
            if self.__token_stream.token_type() != TokenType.SYMBOL:
                return False
            if self.__token_stream.symbol() not in valid_op:
                return False
            return True

        self.__tag("expression")
        self.__ind_level += 1

        # term
        if not self.compile_term():
            self.__token_stream.advance()

        # (op term)*
        while is_op():
            op = self.__token_stream.symbol()
            self.__w_symbol(op)
            self.__token_stream.advance()
            if not self.compile_term():
                self.__token_stream.advance()

        self.__ind_level -= 1
        self.__tag("expression", end=True)
        return True

    def compile_term(self):
        """ term => integerConstant | stringConstant | keywordConstant | varName
        | varName '[' expression ']' | subroutineCall | '(' expression ')' |
        unaryOp term
        returns True if there was a trailing token stream advance"""
        self.__tag("term")
        self.__ind_level += 1

        val = self.__token_stream.token_type()
        trailing_tok = False
        if val == TokenType.INT_CONST:
            # integerConstant
            self.__w_int()
        elif val == TokenType.STRING_CONST:
            # stringConstant
            self.__w_str()
        elif val == TokenType.KEYWORD:
            # keywordConstant
            keyword_constants = [KeyWordType.TRUE,
                                 KeyWordType.FALSE,
                                 KeyWordType.NULL,
                                 KeyWordType.THIS]
            kw = self.__token_stream.key_word()
            if kw in keyword_constants:
                self.__w_keyword(kw)
            else:
                raise Exception(f"Invalid keyword '{kw}' in 'term'")
        elif val == TokenType.SYMBOL:
            unary_ops = ["-", "~"]
            sym = self.__token_stream.symbol()
            if sym in unary_ops:
                # unaryOp term
                self.__w_symbol(sym)
                self.__token_stream.advance()
                trailing_tok = self.compile_term()
            elif sym == "(":
                # '(' expression ')'
                self.__w_symbol(sym)
                self.__token_stream.advance()
                if not self.compile_expression():
                    self.__token_stream.advance()
                self.__w_symbol(")")
            else:
                raise Exception(f"Invalid symbol '{sym}' in 'term'")
        elif val == TokenType.IDENTIFIER:
            # varName | varName '[' expression ']' | subroutineCall
            self.__w_identifier()
            self.__token_stream.advance()
            val = self.__token_stream.token_type()
            if val == TokenType.SYMBOL and self.__w_symbol("["):
                self.__token_stream.advance()
                if not self.compile_expression():
                    self.__token_stream.advance()
                self.__w_symbol("]")
            elif val == TokenType.SYMBOL and self.__w_symbol("("):
                # subroutineCall case 1
                self.__token_stream.advance()
                self.compile_expression_list()
                self.__token_stream.advance()
                self.__w_symbol(")")
            elif val == TokenType.SYMBOL and self.__w_symbol("."):
                # subroutineCall case 2
                self.__token_stream.advance()
                self.__w_identifier()
                self.__token_stream.advance()
                self.__w_symbol("(")
                self.__token_stream.advance()
                self.compile_expression_list()
                self.__w_symbol(")")
            else:
                trailing_tok = True
        else:
            raise Exception(f"Invalid starting token '{val}' for 'term'")

        self.__ind_level -= 1
        self.__tag("term", end=True)
        return trailing_tok

    def compile_expression_list(self) -> bool:
        """ expressionList => (expression (',' expression)* )?
        returns True if there was a trailing token stream advance"""
        self.__tag("expressionList")
        self.__ind_level += 1

        if (self.__token_stream.token_type() == TokenType.SYMBOL
                and self.__token_stream.symbol() == ")"):
            self.__ind_level -= 1
            self.__tag("expressionList", end=True)
            return True

        if not self.compile_expression():
            self.__token_stream.advance()

        while self.__token_stream.token_type() == TokenType.SYMBOL:
            if self.__token_stream.symbol() != ",":
                break
            self.__w_symbol(",")
            self.__token_stream.advance()
            if not self.compile_expression():
                self.__token_stream.advance()

        self.__ind_level -= 1
        self.__tag("expressionList", end=True)
        return True


if __name__ == "__main__":
    with open("test_files/test_in.jack", "r") as infile:
        with open("test_files/test_out.xml", "w") as outfile:
            t = JackTokenizer(infile)
            c = CompilationEngine(t, outfile)
            c.compile_class()
