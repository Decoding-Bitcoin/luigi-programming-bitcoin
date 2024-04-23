from _1_field_element import FieldElement
from _2_point import Point


class TestEcc:
    def test_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)
        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            try:
                Point(x, y, a, b)
                assert False
            except:
                assert True

    def test_add(self):
        prime = 223
        a = FieldElement(num=0, prime=prime)
        b = FieldElement(num=7, prime=prime)
        x1 = FieldElement(num=192, prime=prime)
        y1 = FieldElement(num=105, prime=prime)
        x2 = FieldElement(num=17, prime=prime)
        y2 = FieldElement(num=56, prime=prime)
        p1 = Point(x1, y1, a, b)
        p2 = Point(x2, y2, a, b)
        assert p1 + p2 == Point(
            FieldElement(170, prime), FieldElement(142, prime), a, b
        )

    def test_point_rmul(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(15, prime)
        y = FieldElement(86, prime)
        p = Point(x, y, a, b)
        assert 7 * p == p + p + p + p + p + p + p
