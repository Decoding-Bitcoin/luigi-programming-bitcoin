from _2_point import Point


class TestPoint:

    def test_init(self):
        p1 = Point(-1, -1, 5, 7)
        assert p1.x == -1
        assert p1.y == -1
        assert p1.a == 5
        assert p1.b == 7

        try:
            not_in_curve = Point(-1, -2, 5, 7)
            assert False
        except:
            assert True

        inf = Point(None, None, 5, 7)
        assert inf.x is None
        assert inf.y is None

    def test_eq(self):
        p1 = Point(-1, -1, 5, 7)
        p2 = Point(-1, -1, 5, 7)
        assert p1 == p2

    def test_add_inverse(self):
        p1 = Point(-1, -1, 5, 7)
        p2 = Point(-1, 1, 5, 7)
        inf = Point(None, None, 5, 7)
        assert p1 + p2 == inf

    def test_add_for_different_x(self):
        p1 = Point(2, 5, 5, 7)
        p2 = Point(-1, -1, 5, 7)
        assert p1 + p2 == Point(3, -7, 5, 7)

    def test_add_for_same_point(self):
        p1 = Point(-1, -1, 5, 7)
        assert p1 + p1 == Point(18, 77, 5, 7)
