from ecc import FieldElement, Point, S256Point, Signature, PrivateKey


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

    def test_add_2(self):
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

    def test_point_rmul(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(15, prime)
        y = FieldElement(86, prime)
        p = Point(x, y, a, b)
        assert 7 * p == p + p + p + p + p + p + p


class TestS256Field:
    def test_g_order(self):
        assert S256Point.N * S256Point.G() == S256Point.infinity()

    def test_verify_1(self):
        z = 0xEC208BAA0FC1C19F708A9CA96FDEFF3AC3F230BB4A7BA4AEDE4942AD003C0F60
        p = S256Point(
            0x887387E452B8EACC4ACFDE10D9AAF7F6D9A0F975AABB10D006E4DA568744D06C,
            0x61DE6D95231CD89026E286DF3B6AE4A894A3378E393E93A0F45B666329A0AE34,
        )
        sig = Signature(
            r=0xAC8D1C87E51D0D441BE8B3DD5B05C8795B48875DFFE00B7FFCFAC23010D3A395,
            s=0x68342CEFF8935EDEDD102DD876FFD6BA72D6A427A3EDB13D26EB0781CB423C4,
        )
        assert p.verify(z, sig)

    def test_verify_2(self):
        z = 0x7C076FF316692A3D7EB3C3BB0F8B1488CF72E1AFCD929E29307032997A838A3D
        p = S256Point(
            0x887387E452B8EACC4ACFDE10D9AAF7F6D9A0F975AABB10D006E4DA568744D06C,
            0x61DE6D95231CD89026E286DF3B6AE4A894A3378E393E93A0F45B666329A0AE34,
        )
        sig = Signature(
            r=0xEFF69EF2B1BD93A66ED5219ADD4FB51E11A840F404876325A1E8FFE0529A2C,
            s=0xC7207FEE197D27C618AEA621406F6BF5EF6FCA38681D82B2F06FDDBDCE6FEAB6,
        )
        assert p.verify(z, sig)

    def test_verify_3(self):
        z = 0x7C076FF316692A3D7EB3C3BB0F8B1488CF72E1AFCD929E29307032997A838A3D
        p = S256Point(
            0x887387E452B8EACC4ACFDE10D9AAF7F6D9A0F975AABB10D006E4DA568744D06C,
            0x61DE6D95231CD89026E286DF3B6AE4A894A3378E393E93A0F45B666329A0AE34,
        )
        sig = Signature(
            r=0xEFF69EF2B1BD93A66ED5219ADD4FB51E11A840F404876325A1E8FFE0529A2C,
            s=0xC7207FEE197D27C618AEA621406F6BF5EF6FCA38681D82B2F06FDDBDCE6FEAB5,
        )
        assert not p.verify(z, sig)


class TestPrivateKey:
    def test_sign(self):
        z = 0xEC208BAA0FC1C19F708A9CA96FDEFF3AC3F230BB4A7BA4AEDE4942AD003C0F60
        pk = PrivateKey(5000)
        sig = pk.sign(z)
        assert pk.point.verify(z, sig)
