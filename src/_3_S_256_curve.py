from _1_field_element import FieldElement
from _2_point import Point


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
