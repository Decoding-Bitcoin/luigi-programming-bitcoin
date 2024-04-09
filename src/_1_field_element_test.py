from _1_field_element import FieldElement


class TestFieldElement:

    def test_eq(self):
        a = FieldElement(7, 13)
        b = FieldElement(6, 13)
        assert a != b
        assert a == a
