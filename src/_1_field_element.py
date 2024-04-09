class FieldElement:
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = "Num {} not in field range 0 to {}".format(num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return "FieldElement_{}({})".format(self.prime, self.num)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __neq__(self, other):
        return not (self == other)

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot add two numbers in different Fields")
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot subtract two numbers in different Fields")
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot multiply two numbers in different Fields")
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent):
        # make exponent positive; # page 18
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)  # is more efficient than (x**y) % z
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        """
        Division is multiplying by the inverse of the other number.

        The inverse of a number in finite field is the number raised to the
        power of prime - 2.

        Example in finite field F_19:
        2 / 7 = 2 * 1/7 = 2 * 7 ** (19 - 2) = 2 * 7 ** 17
        """
        if self.prime != other.prime:
            raise TypeError("Cannot divide two numbers in different Fields")
        num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(num, self.prime)
