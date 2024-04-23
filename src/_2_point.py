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
