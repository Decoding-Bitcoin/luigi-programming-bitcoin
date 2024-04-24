"""
File to implement the Elliptic Curve Cryptography presents in the book
"Programming Bitcoin: Learn How to Program Bitcoin from Scratch" by Jimmy Song
"""

import hmac
import hashlib


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
        power of prime - 2. (page 15)

        Example in finite field F_19:
        2 / 7 = 2 * 1/7 = 2 * 7 ** (19 - 2) = 2 * 7 ** 17
        """
        if self.prime != other.prime:
            raise TypeError("Cannot divide two numbers in different Fields")
        num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(num, self.prime)


class Point:
    """
    This class represents a point in an elliptic curve y^2 = x^3 + a*x + b
    """

    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        if self.x is None and self.y is None:
            return
        if self.y**2 != self.x**3 + a * x + b:
            raise ValueError("({}, {}) is not on the curve".format(x, y))

    @staticmethod
    def infinity(a, b):
        return Point(None, None, a, b)

    def __repr__(self) -> str:
        if self.x is None:
            return "Point_{}_{}(infinity)".format(self.a, self.b)
        else:
            return "Point_{}_{}({}, {})".format(self.a, self.b, self.x, self.y)

    def __eq__(self, other):
        return (
            self.x == other.x
            and self.y == other.y
            and self.a == other.a
            and self.b == other.b
        )

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError(
                "Points {}, {} are not on the same curve".format(self, other)
            )
        if self.x is None:
            return other
        if other.x is None:
            return self
        # Case they have they are the additive inverse (p.34)
        if self.x == other.x and self.y != other.y:
            inf = Point(None, None, self.a, self.b)
            return inf
        # Case they are the same point (p.37)
        if self == other:
            x_2 = self.x**2
            s = (x_2 + x_2 + x_2 + self.a) / (self.y + self.y)
        else:
            s = (other.y - self.y) / (other.x - self.x)
        x = s**2 - self.x - other.x
        y = s * (self.x - x) - self.y
        return self.__class__(x, y, self.a, self.b)

    def __rmul__(self, coefficient):
        coef = coefficient
        current = self
        result = self.__class__(None, None, self.a, self.b)
        while coef:
            if coef & 1:
                result += current
            current += current
            coef >>= 1
        return result


class S256Field(FieldElement):
    P = 2**256 - 2**32 - 977

    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=S256Field.P)

    def __repr__(self):
        return "{:x}".format(self.num).zfill(64)


class S256Point(Point):
    A = 0

    B = 7

    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(S256Point.A), S256Field(S256Point.B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        else:
            super().__init__(x, y, a, b)

    def __repr__(self):
        if self.x is None:
            return "S256Point(infinity)"
        else:
            return "S256Point({}, {})".format(self.x, self.y)

    def __rmul__(self, coefficient):
        coef = coefficient % S256Point.N
        return super().__rmul__(coef)

    @staticmethod
    def G():
        return S256Point(
            0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
            0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
        )

    @staticmethod
    def infinity():
        return S256Point(None, None)

    def verify(self, z, sig):
        s_inv = pow(sig.s, S256Point.N - 2, S256Point.N)
        u = z * s_inv % S256Point.N
        v = sig.r * s_inv % S256Point.N
        total = u * S256Point.G() + v * self
        return total.x.num == sig.r


class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return "Signature({:x},{:x})".format(self.r, self.s)


class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * S256Point.G()

    def hex(self):
        return "{:x}".format(self.secret).zfill(64)

    def sign(self, z):
        k = self.deterministic_k(z)
        r = (k * S256Point.G()).x.num  # type: ignore
        k_inv = pow(k, S256Point.N - 2, S256Point.N)
        s = (z + r * self.secret) * k_inv % S256Point.N
        if s > S256Point.N / 2:
            s = S256Point.N - s
        return Signature(r, s)

    def deterministic_k(self, z):
        k = b"\x00" * 32
        v = b"\x01" * 32
        if z > S256Point.N:
            z -= S256Point.N
        z_bytes = z.to_bytes(32, "big")
        secret_bytes = self.secret.to_bytes(32, "big")
        s256 = hashlib.sha256
        k = hmac.new(k, v + b"\x00" + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b"\x01" + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, "big")
            if candidate >= 1 and candidate < S256Point.N:
                return candidate
            k = hmac.new(k, v + b"\x00", s256).digest()
            v = hmac.new(k, v, s256).digest()
