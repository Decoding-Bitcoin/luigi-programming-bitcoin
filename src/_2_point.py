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
            s = (3 * self.x**2 + self.a) / (2 * self.y)
        else:
            s = other.y - self.y / other.x - self.x
        x = s**2 - self.x - other.x
        y = s * (self.x - x) - self.y
        return Point(x, y, self.a, self.b)
