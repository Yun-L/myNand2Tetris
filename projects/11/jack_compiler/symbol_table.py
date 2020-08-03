from custom_types import Kind


class SymbolTable():

    def __init__(self):
        self.__class_scope = {}
        self.__subroutine_scope = {}
        """ Example table entry
        {"identifier_name":
            {"type": "int"
             "kind": Kind.STATIC
            }"index": 0
        }"""
        return

    def start_subroutine(self):
        """ resets subroutine scope """
        self.__subroutine_scope.clear()
        return

    def define(self, name: str, var_type: str, kind: Kind):
        """ defines new identifier of a given name, type and kind and assigns
        it a running index """
        curr_scope = None
        if kind == Kind.STATIC or kind == Kind.FIELD:
            curr_scope = self.__class_scope
        elif kind == Kind.ARG or kind == Kind.VAR:
            curr_scope = self.__subroutine_scope
        else:
            raise Exception(f"'{kind}' not a valid 'Kind'")

        curr_scope[name] = {"type": var_type,
                            "kind": kind,
                            "index": self.var_count(kind)}
        return

    def var_count(self, kind) -> int:
        """ returns the number of variables of the given kind aleady defined
        in the current scope """
        curr_scope = None
        if kind in [Kind.STATIC, Kind.FIELD]:
            curr_scope = self.__class_scope
        elif kind in [Kind.ARG, Kind.VAR]:
            curr_scope = self.__subroutine_scope
        else:
            raise Exception(f"'{kind}' not a valid 'Kind'")

        count = 0

        for d in curr_scope.values():
            if d["kind"] == kind:
                count += 1

        return count

    def get_kind(self, name: str) -> Kind:
        """ returns the kind of the named identifier in the current scope
        returns None if the identifier is unkown"""
        curr_scope = self.__subroutine_scope.get(name, None)

        if not curr_scope:
            curr_scope = self.__class_scope.get(name, None)

        if curr_scope:
            curr_scope = curr_scope["kind"]

        return curr_scope

    def get_type(self, name: str) -> str:
        """ returns the type of the named identifier in the current scope """
        curr_scope = self.__subroutine_scope.get(name, None)

        if not curr_scope:
            curr_scope = self.__class_scope.get(name, None)

        if not curr_scope:
            raise Exception(f"no identifier '{name}' found in current scope.")

        return curr_scope["type"]

    def get_index(self, name: str) -> int:
        """ returns the index assigned to the named identifier """
        curr_scope = self.__subroutine_scope.get(name, None)

        if not curr_scope:
            curr_scope = self.__class_scope.get(name, None)

        if not curr_scope:
            raise Exception(f"no identifier '{name}' found in current scope.")

        return curr_scope["index"]
