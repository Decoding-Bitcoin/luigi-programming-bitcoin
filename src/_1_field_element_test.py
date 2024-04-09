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
