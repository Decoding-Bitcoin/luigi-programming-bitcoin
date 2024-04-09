from _1_field_element import FieldElement


class TestFieldElement:

    def test_eq(self):
        a = FieldElement(7, 13)
        assert a == a

    def test_neq(self):
        a = FieldElement(7, 13)
        b = FieldElement(6, 13)
        assert a != b

    def test_add(self):
        a = FieldElement(7, 13)
        b = FieldElement(12, 13)
        c = FieldElement(6, 13)
        assert a + b == c

    def test_sub(self):
        a = FieldElement(7, 13)
        b = FieldElement(12, 13)
        c = FieldElement(8, 13)
        assert a - b == c

    def test_mul(self):
        a = FieldElement(3, 13)
        b = FieldElement(12, 13)
        c = FieldElement(10, 13)
        assert a * b == c

    def test_pow(self):
        a = FieldElement(3, 13)
        b = FieldElement(1, 13)
        assert a**3 == b

    def test_truediv(self):
        a = FieldElement(2, 19)
        b = FieldElement(7, 19)
        c = FieldElement(3, 19)
        assert a / b == c

    def test_negative_pow(self):
        a = FieldElement(7, 13)
        b = FieldElement(8, 13)
        assert a**-3 == b
