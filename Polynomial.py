from typing import List, Dict


class Polynomial:
    """
    This is a multivariable polynomial class. It is expressed as a multidimensional array, indexed artificially.
    """

    def __init__(self, degrees: Dict[str, int] = None, coeff: List[int] = None, Z: int = None):
        if Z is not None:
            self.coefficients = [Z]
            self.degree = {}
            return

        if coeff is None:
            coeff = [0]
        if degrees is None:
            degrees = {}

        self.coefficients = coeff  # This is not a

        self.degree = degrees  # Not true degrees, just array allocation. degree + 1 \leq the degree in this array.

        self.variables = list(self.degree.keys())  # This should be unused; python Dictionaries are ordered anyways.

        # print(repr(self))

    """ ------------------------------------------------------------------------------------------------------------ """
    """ ---------------------------------------- String Parsing Operations ----------------------------------------- """
    """ ------------------------------------------------------------------------------------------------------------ """

    @classmethod
    def from_string(cls, desired: str):
        desired = desired.replace(" ", "")
        desired = desired.replace("-", "+-")
        if desired[:2] == "+-":
            desired = desired[1:]
        terms = desired.split("+")
        res = Polynomial(Z=0)
        # print(terms)
        for i in terms:
            res += cls.term_from_string(i)
        return res

    """
    Transforms ONE TERM into a Polynomial.
    """

    @classmethod
    def term_from_string(cls, desired: str):
        desired = desired.replace(" ", "")
        negative_flag = False
        if desired[0] == "-":
            negative_flag = True
            desired = desired[1:]

        tokens = [""]
        for i in desired:
            if i not in "0123456789^":
                tokens.append("")
            tokens[-1] += i

        integer_coefficient = 1
        if tokens[0] != "":
            integer_coefficient = int(tokens[0])
        if negative_flag:
            integer_coefficient = -integer_coefficient

        deg = {}
        maxdeg = 1
        for i in tokens[1:]:
            if len(i) == 1:
                deg.update({i: 2})
            else:
                # assert i[1] == "^" #TODO: If this doesn't hold then like, stuff might break. But I think this works.
                deg.update({i[0]: int(i[2:]) + 1})
            maxdeg *= deg[i[0]]
        list_coefficients = [0] * maxdeg
        list_coefficients[-1] = integer_coefficient
        # print(deg)
        # print(list_coefficients)

        return Polynomial(degrees=deg, coeff=list_coefficients)

    """ ------------------------------------------------------------------------------------------------------------ """
    """ -------------------------------- Indexing vs Artificial Array Conversions ---------------------------------- """
    """ ------------------------------------------------------------------------------------------------------------ """

    def term_to_idx(self, desired: Dict[str, int], deg: Dict[str, int] = None) -> int:
        res = 0
        if deg is None:  # In this case, just loop through all variables, no check required.
            for i in self.variables[::-1]:  # We already have the keyset.
                res = res * self.degree[i] + desired[i]
        else:
            reverse = list(deg.keys())[::-1]
            for i in reverse:
                res *= deg[i]
                if i in desired:
                    res += desired[i]

        return res

    def idx_to_term(self, index, deg=None) -> Dict[str, int]:
        if deg is None:
            deg = self.degree
        res = {}
        for i in deg:
            res.update({i: index % deg[i]})
            index //= deg[i]
        return res

    """ ------------------------------------------------------------------------------------------------------------ """
    """ --------------------------------------------- Unary Operations --------------------------------------------- """
    """ ------------------------------------------------------------------------------------------------------------ """

    def invert(self):
        final_deg = {}
        final_deg.update(self.degree)
        final_coefficients = [-i for i in self.coefficients]
        return Polynomial(degrees=final_deg, coeff=final_coefficients)

    def copy(self):
        final_deg = {}
        final_deg.update(self.degree)
        final_coefficients = self.coefficients[:]
        return Polynomial(degrees=final_deg, coeff=final_coefficients)

    """ ------------------------------------------------------------------------------------------------------------ """
    """ --------------------------------------------- Binary Operations -------------------------------------------- """
    """ ------------------------------------------------------------------------------------------------------------ """

    def __add__(self, other):
        if type(other) == int:
            res = self.copy()
            res.coefficients[0] += other
            return res
        elif type(other) == Polynomial:
            # Merge degrees.
            final_deg = {}
            final_deg.update(self.degree)
            maxdeg = len(self.coefficients)
            # print(f"maxdeg = {maxdeg}")
            for i in other.degree:
                if i in final_deg:
                    maxdeg = maxdeg // final_deg[i]
                    final_deg[i] = max(self.degree[i], other.degree[i])
                else:
                    final_deg[i] = other.degree[i]
                # print(maxdeg)

                maxdeg *= final_deg[i]
                # print(maxdeg)

            # print(f"maxdeg = {maxdeg}")

            final_coefficients = [0] * maxdeg

            for idx, c in enumerate(self.coefficients):
                rev = self.idx_to_term(idx)
                actual = self.term_to_idx(rev, final_deg)
                final_coefficients[actual] = c

            for idx, c in enumerate(other.coefficients):
                rev = other.idx_to_term(idx)
                actual = other.term_to_idx(rev, final_deg)
                final_coefficients[actual] += c
            return Polynomial(final_deg, final_coefficients)
        else:
            raise TypeError("Polynomials can only be added to int and Polynomials.")

    def __sub__(self, other):
        if type(other) == int:
            return self + (-other)
        elif type(other) == Polynomial:
            return self + (other.invert())
        else:
            raise TypeError("Polynomials can only be subtracted from int and Polynomials.")

    def __mul__(self, other):
        if type(other) == int:
            res = self.copy()
            res.coefficients = [other * i for i in res.coefficients]
            return res
        elif type(other) == Polynomial:
            # print(self.coefficients)
            # print(other.coefficients)
            # Merge degrees.
            final_deg = {}
            final_deg.update(self.degree)
            maxdeg = len(self.coefficients)

            # print(maxdeg)
            for i in other.degree:
                if i in final_deg:
                    maxdeg = maxdeg // final_deg[i]
                    final_deg[i] += other.degree[i] - 1  # -1 because like, offset.
                else:
                    final_deg[i] = other.degree[i]
                maxdeg *= final_deg[i]
            # print(maxdeg)
            # print(final_deg)
            final_coefficients = [0] * maxdeg

            adj_self_coefficients = []
            for idx, c in enumerate(self.coefficients):
                rev = self.idx_to_term(idx)
                adj_self_coefficients.append(self.term_to_idx(rev, final_deg))

            adj_other_coefficients = []
            for idx, c in enumerate(other.coefficients):
                rev = other.idx_to_term(idx)
                adj_other_coefficients.append(other.term_to_idx(rev, final_deg))
            # print(adj_other_coefficients)
            # print(adj_self_coefficients)
            # print("Goose")
            # print(self.coefficients)
            # print(other.coefficients)
            # print(len(adj_other_coefficients))
            # print(len(adj_self_coefficients))
            # print("Goose")
            # print(len(self.coefficients))
            # print(len(other.coefficients))
            for idx, c in zip(adj_self_coefficients, self.coefficients):
                if c == 0:
                    continue
                for idx2, c2 in zip(adj_other_coefficients, other.coefficients):
                    if c2 == 0:
                        continue
                    final_coefficients[idx + idx2] += c * c2
                    # print(final_coefficients[idx+idx2])
                    # print(self.coefficients[c])
                    # print(self.coefficients[c2])

            return Polynomial(final_deg, final_coefficients)
        else:
            raise TypeError("Polynomials can only be multiplied by int and Polynomials.")

    """ ------------------------------------------------------------------------------------------------------------ """
    """ ----------------------------------------- String Representations ------------------------------------------- """
    """ ------------------------------------------------------------------------------------------------------------ """

    def term_to_str(self, idx: int, coefficient: int) -> str:
        assert coefficient != 0
        var = self.idx_to_term(idx)
        res = ""
        if abs(coefficient) != 1:
            res = str(coefficient)
        if coefficient == -1:
            res = "-"

        # print(coefficient)
        # print(var)
        for i in var:
            if var[i] != 0:
                res += i
                if var[i] > 1:
                    res += "^" + str(var[i])
                    # print(str(var[i]))
        # print(res)
        return res

    def __str__(self) -> str:
        return " + ".join(self.term_to_str(i, j) for i, j in enumerate(self.coefficients) if j != 0)

    def __repr__(self) -> str:
        res = "---- Polynomial ----\n"
        res += str(self.coefficients) + "\n"
        res += str(self.degree) + "\n"
        res += str(self.variables)
        return res

    """ ------------------------------------------------------------------------------------------------------------ """
    """ ------------------------------------------------ Test Suite ------------------------------------------------ """
    """ ------------------------------------------------------------------------------------------------------------ """


if __name__ == "__main__":
    number_2 = Polynomial.term_from_string("2")
    print(number_2)
    abc = Polynomial.term_from_string("abc^4")
    print(abc)

    xyz = Polynomial.term_from_string("-123xyz^2")
    print(xyz)
    print(abc + xyz)
    print(abc + abc + abc)

    print(abc * abc)

    print(abc * xyz)

    plus = Polynomial.from_string("a+b")
    minus = Polynomial.from_string("a-b")
    print(plus)
    print(minus)
    print(plus * minus)

    w = Polynomial.from_string("a+b+c")
    x = Polynomial.from_string("a+b-c")
    y = Polynomial.from_string("a-b+c")
    z = Polynomial.from_string("a+b+c")
    print(w * x * y * z) # Heron's Formula!

    while True:
        print(repr(Polynomial.from_string(input())))
