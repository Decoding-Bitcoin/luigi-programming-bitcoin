from _3_signature import PrivateKey


class TestPrivateKey:
    def test_sign(self):
        z = 0xEC208BAA0FC1C19F708A9CA96FDEFF3AC3F230BB4A7BA4AEDE4942AD003C0F60
        pk = PrivateKey(5000)
        sig = pk.sign(z)
        assert pk.point.verify(z, sig)
