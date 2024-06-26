from ecc import FieldElement, Point, S256Point, Signature, PrivateKey, G, N, P
from random import randint


class TestFieldElement:

    def test_ne(self):
        a = FieldElement(2, 31)
        b = FieldElement(2, 31)
        c = FieldElement(15, 31)
        assert a == b
        assert a != c
        assert not (a != b)

    def test_add(self):
        a = FieldElement(2, 31)
        b = FieldElement(15, 31)
        assert a + b == FieldElement(17, 31)
        a = FieldElement(17, 31)
        b = FieldElement(21, 31)
        assert a + b == FieldElement(7, 31)

    def test_sub(self):
        a = FieldElement(29, 31)
        b = FieldElement(4, 31)
        assert a - b == FieldElement(25, 31)
        a = FieldElement(15, 31)
        b = FieldElement(30, 31)
        assert a - b == FieldElement(16, 31)

    def test_mul(self):
        a = FieldElement(24, 31)
        b = FieldElement(19, 31)
        assert a * b == FieldElement(22, 31)

    def test_rmul(self):
        a = FieldElement(24, 31)
        b = 2
        assert b * a == a + a

    def test_pow(self):
        a = FieldElement(17, 31)
        assert a**3 == FieldElement(15, 31)
        a = FieldElement(5, 31)
        b = FieldElement(18, 31)
        assert a**5 * b == FieldElement(16, 31)

    def test_div(self):
        a = FieldElement(3, 31)
        b = FieldElement(24, 31)
        assert a / b == FieldElement(4, 31)
        a = FieldElement(17, 31)
        assert a**-3 == FieldElement(29, 31)
        a = FieldElement(4, 31)
        b = FieldElement(11, 31)
        assert a**-4 * b == FieldElement(13, 31)


class TestPoint:

    def test_ne(self):
        a = Point(x=3, y=-7, a=5, b=7)
        b = Point(x=18, y=77, a=5, b=7)
        assert a != b
        assert not (a != a)

    def test_on_curve(self):
        try:
            Point(x=-2, y=4, a=5, b=7)
            assert False
        except ValueError:
            pass
        Point(x=3, y=-7, a=5, b=7)
        Point(x=18, y=77, a=5, b=7)

    def test_add0(self):
        a = Point(x=None, y=None, a=5, b=7)
        b = Point(x=2, y=5, a=5, b=7)
        c = Point(x=2, y=-5, a=5, b=7)
        assert a + b == b
        assert b + a == b
        assert b + c == a

    def test_add1(self):
        a = Point(x=3, y=7, a=5, b=7)
        b = Point(x=-1, y=-1, a=5, b=7)
        assert a + b == Point(x=2, y=-5, a=5, b=7)

    def test_add2(self):
        a = Point(x=-1, y=1, a=5, b=7)
        assert a + a == Point(x=18, y=-77, a=5, b=7)


class TestS256Field:

    def test_order(self):
        point = N * G
        assert point.x == None

    def test_pubpoint(self):
        # write a test that tests the public point for the following
        points = (
            # secret, x, y
            (
                7,
                0x5CBDF0646E5DB4EAA398F365F2EA7A0E3D419B7E0330E39CE92BDDEDCAC4F9BC,
                0x6AEBCA40BA255960A3178D6D861A54DBA813D0B813FDE7B5A5082628087264DA,
            ),
            (
                1485,
                0xC982196A7466FBBBB0E27A940B6AF926C1A74D5AD07128C82824A11B5398AFDA,
                0x7A91F9EAE64438AFB9CE6448A1C133DB2D8FB9254E4546B6F001637D50901F55,
            ),
            (
                2**128,
                0x8F68B9D2F63B5F339239C1AD981F162EE88C5678723EA3351B7B444C9EC4C0DA,
                0x662A9F2DBA063986DE1D90C2B6BE215DBBEA2CFE95510BFDF23CBF79501FFF82,
            ),
            (
                2**240 + 2**31,
                0x9577FF57C8234558F293DF502CA4F09CBC65A6572C842B39B366F21717945116,
                0x10B49C67FA9365AD7B90DAB070BE339A1DAF9052373EC30FFAE4F72D5E66D053,
            ),
        )

        # iterate over points
        for secret, x, y in points:
            # initialize the secp256k1 point (S256Point)
            point = S256Point(x, y)
            # check that the secret*G is the same as the point
            assert secret * G == point

    def test_verify(self):
        point = S256Point(
            0x887387E452B8EACC4ACFDE10D9AAF7F6D9A0F975AABB10D006E4DA568744D06C,
            0x61DE6D95231CD89026E286DF3B6AE4A894A3378E393E93A0F45B666329A0AE34,
        )
        z = 0xEC208BAA0FC1C19F708A9CA96FDEFF3AC3F230BB4A7BA4AEDE4942AD003C0F60
        r = 0xAC8D1C87E51D0D441BE8B3DD5B05C8795B48875DFFE00B7FFCFAC23010D3A395
        s = 0x68342CEFF8935EDEDD102DD876FFD6BA72D6A427A3EDB13D26EB0781CB423C4
        assert point.verify(z, Signature(r, s))
        z = 0x7C076FF316692A3D7EB3C3BB0F8B1488CF72E1AFCD929E29307032997A838A3D
        r = 0xEFF69EF2B1BD93A66ED5219ADD4FB51E11A840F404876325A1E8FFE0529A2C
        s = 0xC7207FEE197D27C618AEA621406F6BF5EF6FCA38681D82B2F06FDDBDCE6FEAB6
        assert point.verify(z, Signature(r, s))

    def test_sec(self):
        coefficient = 999**3
        uncompressed = "049d5ca49670cbe4c3bfa84c96a8c87df086c6ea6a24ba6b809c9de234496808d56fa15cc7f3d38cda98dee2419f415b7513dde1301f8643cd9245aea7f3f911f9"
        compressed = (
            "039d5ca49670cbe4c3bfa84c96a8c87df086c6ea6a24ba6b809c9de234496808d5"
        )
        point = coefficient * G
        assert point.sec(compressed=False), bytes.fromhex(uncompressed)
        assert point.sec(compressed=True), bytes.fromhex(compressed)
        coefficient = 123
        uncompressed = "04a598a8030da6d86c6bc7f2f5144ea549d28211ea58faa70ebf4c1e665c1fe9b5204b5d6f84822c307e4b4a7140737aec23fc63b65b35f86a10026dbd2d864e6b"
        compressed = (
            "03a598a8030da6d86c6bc7f2f5144ea549d28211ea58faa70ebf4c1e665c1fe9b5"
        )
        point = coefficient * G
        assert point.sec(compressed=False) == bytes.fromhex(uncompressed)
        assert point.sec(compressed=True) == bytes.fromhex(compressed)
        coefficient = 42424242
        uncompressed = "04aee2e7d843f7430097859e2bc603abcc3274ff8169c1a469fee0f20614066f8e21ec53f40efac47ac1c5211b2123527e0e9b57ede790c4da1e72c91fb7da54a3"
        compressed = (
            "03aee2e7d843f7430097859e2bc603abcc3274ff8169c1a469fee0f20614066f8e"
        )
        point = coefficient * G
        assert point.sec(compressed=False) == bytes.fromhex(uncompressed)
        assert point.sec(compressed=True) == bytes.fromhex(compressed)

    def test_address(self):
        secret = 888**3
        mainnet_address = "148dY81A9BmdpMhvYEVznrM45kWN32vSCN"
        testnet_address = "mieaqB68xDCtbUBYFoUNcmZNwk74xcBfTP"
        point = secret * G
        assert point.address(compressed=True, testnet=False) == mainnet_address
        assert point.address(compressed=True, testnet=True) == testnet_address
        secret = 321
        mainnet_address = "1S6g2xBJSED7Qr9CYZib5f4PYVhHZiVfj"
        testnet_address = "mfx3y63A7TfTtXKkv7Y6QzsPFY6QCBCXiP"
        point = secret * G
        assert point.address(compressed=False, testnet=False) == mainnet_address
        assert point.address(compressed=False, testnet=True) == testnet_address
        secret = 4242424242
        mainnet_address = "1226JSptcStqn4Yq9aAmNXdwdc2ixuH9nb"
        testnet_address = "mgY3bVusRUL6ZB2Ss999CSrGVbdRwVpM8s"
        point = secret * G
        assert point.address(compressed=False, testnet=False) == mainnet_address
        assert point.address(compressed=False, testnet=True) == testnet_address


class TestSignature:

    def test_der(self):
        testcases = (
            (1, 2),
            (randint(0, 2**256), randint(0, 2**255)),
            (randint(0, 2**256), randint(0, 2**255)),
        )
        for r, s in testcases:
            sig = Signature(r, s)
            der = sig.der()
            sig2 = Signature.parse(der)
            assert sig2.r == r
            assert sig2.s == s


class TestPrivateKey:
    def test_sign(self):
        z = 0xEC208BAA0FC1C19F708A9CA96FDEFF3AC3F230BB4A7BA4AEDE4942AD003C0F60
        pk = PrivateKey(5000)
        sig = pk.sign(z)
        assert pk.point.verify(z, sig)
