__author__ = "Yun-L"


class Code(object):
    """Translates assembly language mnemonics into binary codes"""

    def __init__(self, dest, jump, comp):
        self.__dest = dest
        self.__jump = jump
        self.__comp = comp

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

        return "".join(dest_bits)

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
            "JMP": "111"
        }

        return jump_bits[jump]

    @comp.setter
    def comp(self, comp):
        return "TODO"
