__author__ = "Yun-L"


class Code(object):
    """Translates assembly language mnemonics into binary codes"""

    def __init__(self, dest, jump, comp):
        self.dest = dest
        self.jump = jump
        self.comp = comp

    @property
    def dest(self):
        return self.__dest

    @property
    def jump(self):
        return self.__jump

    @property
    def comp(self):
        return self.__comp

    @dest.setter
    def dest(self, dest):

        dest_bits = ["0", "0", "0"]

        if "A" in dest:
            dest_bits[0] = "1"

        if "D" in dest:
            dest_bits[1] = "1"

        if "M" in dest:
            dest_bits[2] = "1"

        self.__dest = "".join(dest_bits)

    @jump.setter
    def jump(self, jump):

        jump_bits = {
            "": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"}
        if jump in jump_bits:
            self.__jump = jump_bits[jump]
        else:
            raise Exception("[{}] is not a valid 'jump' token.".format(jump))

    @comp.setter
    def comp(self, comp):
        try:
            if len(comp) == 1:
                self.__comp = self.__comp1(comp)
            elif len(comp) == 2:
                self.__comp = self.__comp2(comp)
            elif len(comp) == 3:
                self.__comp = self.__comp3(comp)
            else:
                raise Exception(
                    "[{}] is not a valid 'comp' token".format(comp))
        except:
            raise Exception("[{}] is not a valid 'comp' token".format(comp))

    def __comp1(self, comp):
        """ Returns bits for comp tokens of length 1 """
        bits = {
            "0": "0101010",
            "1": "0111111",
            "D": "0001100",
            "A": "0110000",
            "M": "1110000"}

        if comp in bits:
            return bits[comp]
        else:
            raise Exception("[{}] is not a valid 'comp' token".format(comp))

    def __comp2(self, comp):
        """ Returns bits for comp tokens of length 2 """
        bits = {
            "-1": "0111010",
            "!D": "0001101",
            "!A": "0110001",
            "!M": "1110001",
            "-D": "0001111",
            "-A": "0110011",
            "-M": "1110011"}

        if comp in bits:
            return bits[comp]
        else:
            raise Exception("[{}] is not a valid 'comp' token".format(comp))

    def __comp3(self, comp):
        """ Returns bits for comp tokens of length 3 """
        bits = {
            "D+1": "0011111",
            "A+1": "0110111",
            "M+1": "1110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "M-1": "1110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "D+M": "1000010",
            "D-M": "1010011",
            "A-D": "0000111",
            "M-D": "1000111",
            "D&A": "0000000",
            "D&M": "1000000",
            "D|A": "0010101",
            "D|M": "1010101"}

        if comp in bits:
            return bits[comp]
        else:
            raise Exception("[{}] is not a valid 'comp' token".format(comp))
