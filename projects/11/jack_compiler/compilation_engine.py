from jack_tokenizer import JackTokenizer
from vm_writer import VMWriter
from custom_types import KeyWordType, TokenType, Kind, MemorySegType, ArithCMD
from symbol_table import SymbolTable


class CompilationEngine():
    """Recursive top-down parser"""

    def __init__(self, token_stream: JackTokenizer, output_file_stream):
        self.__token_stream = token_stream
        self.__vm_w = VMWriter(output_file_stream)
        self.__symbol_table = SymbolTable()
        self.__ident_memos = {}
        self.__if_count = 0
        self.__while_count = 0
        return

    def __get_class_name(self):
        val = self.__ident_memos.get("class_name", None)
        if val is None:
            raise Exception("value for 'class_name' was not set")
        return val

    def __set_class_name(self, val: str):
        self.__ident_memos["class_name"] = val
        return

    def __get_if_labels(self):
        label1 = "".join([self.__get_class_name(),
                         "$if_",
                          str(self.__if_count)])
        label2 = "".join([self.__get_class_name(),
                         "$if_end_",
                          str(self.__if_count)])
        self.__if_count += 1
        return (label1, label2)

    def __get_while_labels(self):
        label1 = "".join([self.__get_class_name(),
                          "$while_",
                          str(self.__while_count)])
        label2 = "".join([self.__get_class_name(),
                          "$while_end_",
                          str(self.__while_count)])
        self.__while_count += 1
        return (label1, label2)

    def compile_class(self):
        # 'class'
        self.__token_stream.advance()
        # className
        self.__token_stream.advance()
        self.__set_class_name(self.__token_stream.identifier())
        # '{'
        self.__token_stream.advance()
        #
        self.__token_stream.advance()
        while self.compile_class_var_dec():
            self.__token_stream.advance()
        while self.compile_subroutine():
            self.__token_stream.advance()
        # '}'
        return

    def compile_class_var_dec(self) -> True:
        """ classVarDec => ('static' | 'field') type varName (',' varName)* ';'
        Returns False if first token is invalid, True otherwise. """
        if self.__token_stream.token_type() != TokenType.KEYWORD:
            return False

        val = self.__token_stream.key_word()
        if val != KeyWordType.STATIC and val != KeyWordType.FIELD:
            return False

        # static | field
        kind = self.__token_stream.key_word().value
        if kind == "static":
            kind = Kind.STATIC
        elif kind == "field":
            kind = Kind.FIELD

        # type => int | char | boolean | className
        self.__token_stream.advance()
        if self.__token_stream.token_type() == TokenType.KEYWORD:
            accept_lst = [KeyWordType.INT,
                          KeyWordType.CHAR,
                          KeyWordType.BOOLEAN]

            val = self.__token_stream.key_word()
            if val not in accept_lst:
                raise Exception(f"'{val}' not a valid keyword for 'type'")
            vtype = self.__token_stream.key_word().value
        else:
            vtype = self.__token_stream.identifier()

        # varName
        self.__token_stream.advance()
        name = self.__token_stream.identifier()
        self.__symbol_table.define(name, vtype, kind)

        # (',' varName)*
        self.__token_stream.advance()
        while self.__token_stream.symbol() == ",":
            self.__token_stream.advance()
            # varName
            name = self.__token_stream.identifier()
            self.__symbol_table.define(name, vtype, kind)
            self.__token_stream.advance()
        # ;
        return True

    def compile_subroutine(self) -> True:
        """ subroutineDec => ('constructor' | 'function' | 'method')
        ( 'void' | type) subroutineName '(' parameterList ')' subroutineBody
        Returns True if successful, False otherwise. """

        self.__symbol_table.start_subroutine()

        if self.__token_stream.token_type() != TokenType.KEYWORD:
            return False

        # 'constructor' | 'function' | 'method'
        func_type = self.__token_stream.key_word()
        func_types = [KeyWordType.CONSTRUCTOR,
                      KeyWordType.FUNCTION,
                      KeyWordType.METHOD]
        if func_type not in func_types:
            return False

        # 'void' | type => ('int' | 'char' | 'boolean' | className)
        self.__token_stream.advance()
        if self.__token_stream.token_type() == TokenType.KEYWORD:
            accept_lst = [KeyWordType.INT,
                          KeyWordType.CHAR,
                          KeyWordType.BOOLEAN,
                          KeyWordType.VOID]

            kw = self.__token_stream.key_word()
            if kw not in accept_lst:
                raise Exception(
                    f"'{kw}' not a valid keyword for 'void' or 'type'")
        elif self.__token_stream.token_type() == TokenType.IDENTIFIER:
            # className
            pass
        else:
            raise Exception("Must be void or 'type'")

        # subroutineName
        self.__token_stream.advance()
        func_name = "".join([self.__get_class_name(), ".",
                             self.__token_stream.identifier()])
        # '('
        self.__token_stream.advance()

        # parameterList
        if func_type == KeyWordType.METHOD:
            self.__symbol_table.define("this",
                                       self.__get_class_name(),
                                       Kind.ARG)

        self.__token_stream.advance()
        self.compile_parameter_list()
        # ')'

        # subroutineBody
        # '{'
        self.__token_stream.advance()

        # varDec*
        self.__token_stream.advance()
        while self.compile_var_dec():
            self.__token_stream.advance()

        num_locals = self.__symbol_table.var_count(Kind.VAR)
        self.__vm_w.write_function(func_name, num_locals)

        if func_type == KeyWordType.METHOD:
            self.__vm_w.write_push(MemorySegType.ARGUMENT, 0)
            self.__vm_w.write_pop(MemorySegType.POINTER, 0)
        elif func_type == KeyWordType.CONSTRUCTOR:
            obj_size = self.__symbol_table.var_count(Kind.FIELD)
            self.__vm_w.write_push(MemorySegType.CONSTANT, obj_size)
            self.__vm_w.write_call("Memory.alloc", 1)
            self.__vm_w.write_pop(MemorySegType.POINTER, 0)

            # statements
        if not self.compile_statements():
            self.__token_stream.advance()

        # '}'

        return True

    def compile_parameter_list(self) -> bool:
        """ parameterList => ((type varName) (',' type varName)*)?
        returns the number of parameters. Will have a trailing advance()"""
        tok_type = self.__token_stream.token_type()
        # check if first token is 'type'
        if tok_type == TokenType.KEYWORD:
            accept_lst = [KeyWordType.INT,
                          KeyWordType.CHAR,
                          KeyWordType.BOOLEAN]

            val = self.__token_stream.key_word()
            if val not in accept_lst:
                raise Exception(f"'{val}' not a valid keyword for 'type'")
            vtype = val.value
        elif tok_type == TokenType.IDENTIFIER:
            # className if not int | char | boolean
            vtype = self.__token_stream.identifier()
        else:
            # trailing advance from before the function call
            return 0

        # varName
        self.__token_stream.advance()
        self.__symbol_table.define(self.__token_stream.identifier(),
                                   vtype,
                                   Kind.ARG)

        # (',' type varName)*
        self.__token_stream.advance()
        while self.__token_stream.symbol() == ",":
            # type
            self.__token_stream.advance()
            if self.__token_stream.token_type() == TokenType.KEYWORD:
                accept_lst = [KeyWordType.INT,
                              KeyWordType.CHAR,
                              KeyWordType.BOOLEAN]

                val = self.__token_stream.key_word()
                if val not in accept_lst:
                    raise Exception(f"'{val}' not a valid keyword for 'type'")
                vtype = val.value
            else:
                vtype = self.__token_stream.identifier()

            # varName
            self.__token_stream.advance()
            self.__symbol_table.define(self.__token_stream.identifier(),
                                       vtype,
                                       Kind.ARG)
            self.__token_stream.advance()

        return

    def compile_var_dec(self):
        """ varDec => 'var' type varName (',' varName)* ';'
        Returns True if successful
        Returns False if first token is invalid for varDec"""
        # 'var'
        if self.__token_stream.token_type() != TokenType.KEYWORD:
            return False

        if self.__token_stream.key_word() != KeyWordType.VAR:
            return False

        # type
        self.__token_stream.advance()
        if self.__token_stream.token_type() == TokenType.KEYWORD:
            accept_lst = [KeyWordType.INT,
                          KeyWordType.CHAR,
                          KeyWordType.BOOLEAN]

            kw = self.__token_stream.key_word()
            if kw not in accept_lst:
                raise Exception(f"'{kw}' not a valid keyword for 'type'")
            vtype = kw.value
        else:
            vtype = self.__token_stream.identifier()

        # varName
        self.__token_stream.advance()
        self.__symbol_table.define(self.__token_stream.identifier(),
                                   vtype,
                                   Kind.VAR)

        # (',' varName)*
        self.__token_stream.advance()
        while self.__token_stream.symbol() == ",":
            self.__token_stream.advance()
            self.__symbol_table.define(self.__token_stream.identifier(),
                                       vtype,
                                       Kind.VAR)
            self.__token_stream.advance()
        # ';'
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

        return True

    def compile_if(self):
        """ ifStatement => 'if' '(' expression ')' '{' statements '}' ('else'
        '{' statements '}')?"""

        # 'if'
        # '('
        self.__token_stream.advance()

        # expression
        self.__token_stream.advance()
        if not self.compile_expression():
            self.__token_stream.advance()

        if_labels = self.__get_if_labels()
        self.__vm_w.write_arithmetic(ArithCMD.NOT)
        self.__vm_w.write_if(if_labels[0])

        # ')'
        # '{'
        self.__token_stream.advance()

        # statements
        self.__token_stream.advance()
        if not self.compile_statements():
            self.__token_stream.advance()

        # '}'

        self.__vm_w.write_goto(if_labels[1])

        # ('else' '{' statements '}')?
        self.__vm_w.write_label(if_labels[0])
        self.__token_stream.advance()
        if (self.__token_stream.token_type() == TokenType.KEYWORD
                and self.__token_stream.key_word() == KeyWordType.ELSE):
            self.__token_stream.advance()
            self.__token_stream.advance()
            if not self.compile_statements():
                self.__token_stream.advance()
            trailing_adv = False
        else:
            trailing_adv = True

        self.__vm_w.write_label(if_labels[1])

        return trailing_adv

    def compile_let(self) -> bool:
        """ letStatement => 'let' varName ('[' expression ']')? '=' expression ';'
        returns True if there was a trailing token stream advance
        """

        # 'let'
        # varName
        self.__token_stream.advance()
        dest = self.__token_stream.identifier()
        kind = self.__symbol_table.get_kind(dest)
        ind = self.__symbol_table.get_index(dest)
        is_array = False

        # ('[' expression ']')?
        self.__token_stream.advance()
        if self.__token_stream.symbol() == "[":
            is_array = True
            self.__token_stream.advance()
            if not self.compile_expression():
                self.__token_stream.advance()
            self.__token_stream.advance()
            if kind == Kind.VAR:
                self.__vm_w.write_push(MemorySegType.LOCAL, ind)
            elif kind == Kind.FIELD:
                self.__vm_w.write_push(MemorySegType.THIS, ind)
            elif kind == Kind.ARG:
                self.__vm_w.write_push(MemorySegType.ARGUMENT, ind)
            elif kind == Kind.STATIC:
                self.__vm_w.write_push(MemorySegType.STATIC, ind)
            self.__vm_w.write_arithmetic(ArithCMD.ADD)
            self.__vm_w.write_pop(MemorySegType.TEMP, 1)

        # "="

        # expression
        self.__token_stream.advance()
        if not self.compile_expression():
            self.__token_stream.advance()

        # ";"
        if is_array:
            self.__vm_w.write_push(MemorySegType.TEMP, 1)
            self.__vm_w.write_pop(MemorySegType.POINTER, 1)
            self.__vm_w.write_pop(MemorySegType.THAT, 0)
            return False

        if kind == Kind.VAR:
            self.__vm_w.write_pop(MemorySegType.LOCAL, ind)
        elif kind == Kind.FIELD:
            self.__vm_w.write_pop(MemorySegType.THIS, ind)
        elif kind == Kind.ARG:
            self.__vm_w.write_pop(MemorySegType.ARGUMENT, ind)
        elif kind == Kind.STATIC:
            self.__vm_w.write_pop(MemorySegType.STATIC, ind)

        return False

    def compile_while(self) -> bool:
        """ whileStatement => 'while' '(' expression ')' '{' statements '}'
        returns True if there was a trailing token stream advance"""

        # 'while'
        # '('
        self.__token_stream.advance()
        while_labels = self.__get_while_labels()
        self.__vm_w.write_label(while_labels[0])

        # expression
        self.__token_stream.advance()
        if not self.compile_expression():
            self.__token_stream.advance()

        self.__vm_w.write_arithmetic(ArithCMD.NOT)
        self.__vm_w.write_if(while_labels[1])

        # ')'
        # '{'
        self.__token_stream.advance()

        # statements
        self.__token_stream.advance()
        if not self.compile_statements():
            self.__token_stream.advance()
        self.__vm_w.write_goto(while_labels[0])

        # '}'
        self.__vm_w.write_label(while_labels[1])

        return False

    def compile_do(self) -> bool:
        """ doStatement => 'do' subroutineCall ';'
        returns True if there was a trailing token stream advance"""

        # 'do'
        # subroutineCall
        param_count = 0
        self.__token_stream.advance()
        sub_name = self.__token_stream.identifier()
        self.__token_stream.advance()
        curr_sym = self.__token_stream.symbol()
        if curr_sym == "(":
            # '('
            # method
            sub_name = "".join([self.__get_class_name(),
                                ".",
                                sub_name])
            self.__vm_w.write_push(MemorySegType.POINTER, 0)

            # expressionList
            self.__token_stream.advance()
            param_count += self.compile_expression_list()
            param_count += 1
            # ')'
        elif curr_sym == ".":
            kind = self.__symbol_table.get_kind(sub_name)
            if kind is not None:
                # method -> push reference to object
                ind = self.__symbol_table.get_index(sub_name)
                if kind == Kind.VAR:
                    self.__vm_w.write_push(MemorySegType.LOCAL, ind)
                elif kind == Kind.FIELD:
                    self.__vm_w.write_push(MemorySegType.THIS, ind)
                elif kind == Kind.ARG:
                    self.__vm_w.write_push(MemorySegType.ARGUMENT, ind)
                elif kind == Kind.STATIC:
                    self.__vm_w.write_push(MemorySegType.STATIC, ind)
                param_count += 1
                sub_name = self.__symbol_table.get_type(sub_name)
            else:
                # function or constructor
                pass

            self.__token_stream.advance()
            # subroutineName
            sub_name = "".join([sub_name,
                                ".",
                                self.__token_stream.identifier()])
            self.__token_stream.advance()
            # '('
            self.__token_stream.advance()
            # expressionList
            param_count += self.compile_expression_list()

            # ')'
        else:
            raise Exception(f"Invalid symbol '{curr_sym}'")

        self.__vm_w.write_call(sub_name, param_count)
        self.__vm_w.write_pop(MemorySegType.TEMP, 0)
        self.__token_stream.advance()
        # ';'

        return False

    def compile_return(self) -> bool:
        """ returnStatement => 'return' expression? ';'
        returns True if there was a trailing token stream advance"""

        # 'return'
        # expression?
        self.__token_stream.advance()
        if (self.__token_stream.token_type() != TokenType.SYMBOL
                or self.__token_stream.symbol() != ";"):
            if not self.compile_expression():
                self.__token_stream.advance()
        else:
            self.__vm_w.write_push(MemorySegType.CONSTANT, 0)

        self.__vm_w.write_return()
        # ";"

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

        op_map = {"+": ArithCMD.ADD,
                  "-": ArithCMD.SUB,
                  "&": ArithCMD.AND,
                  "|": ArithCMD.OR,
                  "<": ArithCMD.LT,
                  ">": ArithCMD.GT,
                  "=": ArithCMD.EQ}

        # term
        if not self.compile_term():
            self.__token_stream.advance()

        # (op term)*
        while is_op():
            op = self.__token_stream.symbol()
            self.__token_stream.advance()
            if not self.compile_term():
                self.__token_stream.advance()

            if op == "*":
                self.__vm_w.write_call("Math.multiply", 2)
            elif op == "/":
                self.__vm_w.write_call("Math.divide", 2)
            else:
                self.__vm_w.write_arithmetic(op_map[op])

        return True

    def compile_term(self):
        """ term => integerConstant | stringConstant | keywordConstant | varName
        | varName '[' expression ']' | subroutineCall | '(' expression ')' |
        unaryOp term
        returns True if there was a trailing token stream advance"""

        val = self.__token_stream.token_type()
        trailing_tok = False
        if val == TokenType.INT_CONST:
            # integerConstant
            self.__vm_w.write_push(MemorySegType.CONSTANT,
                                   self.__token_stream.int_val())
        elif val == TokenType.STRING_CONST:
            # stringConstant
            s = self.__token_stream.string_val()
            self.__vm_w.write_push(MemorySegType.CONSTANT, len(s))
            self.__vm_w.write_call("String.new", 1)
            for c in s:
                self.__vm_w.write_push(MemorySegType.CONSTANT, ord(c))
                self.__vm_w.write_call("String.appendChar", 2)

        elif val == TokenType.KEYWORD:
            # keywordConstant
            kw = self.__token_stream.key_word()
            if kw in [KeyWordType.FALSE, KeyWordType.NULL]:
                self.__vm_w.write_push(MemorySegType.CONSTANT, 0)
            elif kw == KeyWordType.TRUE:
                self.__vm_w.write_push(MemorySegType.CONSTANT, 1)
                self.__vm_w.write_arithmetic(ArithCMD.NEG)
            elif kw == KeyWordType.THIS:
                self.__vm_w.write_push(MemorySegType.POINTER, 0)
            else:
                raise Exception(f"Invalid keyword '{kw}' in 'term'")
        elif val == TokenType.SYMBOL:
            unary_ops_map = {"-": ArithCMD.NEG,
                             "~": ArithCMD.NOT}
            sym = self.__token_stream.symbol()
            if sym in unary_ops_map.keys():
                # unaryOp term
                self.__token_stream.advance()
                trailing_tok = self.compile_term()
                self.__vm_w.write_arithmetic(unary_ops_map[sym])
            elif sym == "(":
                # '(' expression ')'
                self.__token_stream.advance()
                if not self.compile_expression():
                    self.__token_stream.advance()
            else:
                raise Exception(f"Invalid symbol '{sym}' in 'term'")
        elif val == TokenType.IDENTIFIER:
            # varName | varName '[' expression ']' | subroutineCall

            name = self.__token_stream.identifier()
            self.__token_stream.advance()
            val = self.__token_stream.token_type()

            if (val == TokenType.SYMBOL and self.__token_stream.symbol() == "["):
                self.__token_stream.advance()
                if not self.compile_expression():
                    self.__token_stream.advance()
                # ']'
                kind = self.__symbol_table.get_kind(name)
                ind = self.__symbol_table.get_index(name)
                if kind == Kind.VAR:
                    self.__vm_w.write_push(MemorySegType.LOCAL, ind)
                elif kind == Kind.ARG:
                    self.__vm_w.write_push(MemorySegType.ARGUMENT, ind)
                elif kind == Kind.FIELD:
                    self.__vm_w.write_push(MemorySegType.THIS, ind)
                elif kind == Kind.STATIC:
                    self.__vm_w.write_push(MemorySegType.STATIC, ind)

                self.__vm_w.write_arithmetic(ArithCMD.ADD)
                self.__vm_w.write_pop(MemorySegType.POINTER, 1)
                self.__vm_w.write_push(MemorySegType.THAT, 0)
            elif (val == TokenType.SYMBOL and
                  self.__token_stream.symbol() == "("):
                # subroutineCall case 1
                self.__token_stream.advance()
                self.__vm_w.write_push(MemorySegType.POINTER, 0)
                arg_count = self.compile_expression_list() + 1
                self.__token_stream.advance()
                # ')'
                name = "".join([self.__get_class_name(), ".", name])
                self.__vm_w.write_call(name, arg_count)
            elif (val == TokenType.SYMBOL and
                  self.__token_stream.symbol() == "."):
                # subroutineCall case 2
                kind = self.__symbol_table.get_kind(name)
                if kind is not None:
                    # method -> push reference to object
                    ind = self.__symbol_table.get_index(name)
                    if kind == Kind.VAR:
                        self.__vm_w.write_push(MemorySegType.LOCAL, ind)
                    elif kind == Kind.FIELD:
                        self.__vm_w.write_push(MemorySegType.THIS, ind)
                    elif kind == Kind.ARG:
                        self.__vm_w.write_push(MemorySegType.ARGUMENT, ind)
                    elif kind == Kind.STATIC:
                        self.__vm_w.write_push(MemorySegType.STATIC, ind)
                    arg_count = 1
                    name = self.__symbol_table.get_type(name)
                else:
                    # function or constructor
                    arg_count = 0

                self.__token_stream.advance()
                # subroutineName
                name = "".join([name, ".", self.__token_stream.identifier()])
                self.__token_stream.advance()
                # '('
                self.__token_stream.advance()
                # expressionList
                arg_count += self.compile_expression_list()
                # ')'
                self.__vm_w.write_call(name, arg_count)
            else:
                trailing_tok = True
                kind = self.__symbol_table.get_kind(name)
                ind = self.__symbol_table.get_index(name)
                if kind == Kind.VAR:
                    self.__vm_w.write_push(MemorySegType.LOCAL, ind)
                elif kind == Kind.STATIC:
                    self.__vm_w.write_push(MemorySegType.STATIC, ind)
                elif kind == Kind.ARG:
                    self.__vm_w.write_push(MemorySegType.ARGUMENT, ind)
                elif kind == Kind.FIELD:
                    self.__vm_w.write_push(MemorySegType.THIS, ind)
        else:
            raise Exception(f"Invalid starting token '{val}' for 'term'")

        return trailing_tok

    def compile_expression_list(self) -> int:
        """ expressionList => (expression (',' expression)* )?
        Always has a trailing token advance.
        Returns the amount of expressions in the list"""

        exp_count = 0

        if (self.__token_stream.token_type() == TokenType.SYMBOL
                and self.__token_stream.symbol() == ")"):
            return exp_count

        if not self.compile_expression():
            self.__token_stream.advance()

        exp_count += 1

        while self.__token_stream.token_type() == TokenType.SYMBOL:
            if self.__token_stream.symbol() != ",":
                break
            # ','
            exp_count += 1
            self.__token_stream.advance()
            if not self.compile_expression():
                self.__token_stream.advance()

        return exp_count
