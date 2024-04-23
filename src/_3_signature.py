import hmac
from _3_S_256_curve import S256Point
import hashlib
from random import randint


class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return "Signature({:x},{:x})".format(self.r, self.s)


class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * S256Point.G()

    def hex(self):
        return "{:x}".format(self.secret).zfill(64)

    def sign(self, z):
        k = self.deterministic_k(z)
        r = (k * S256Point.G()).x.num  # type: ignore
        k_inv = pow(k, S256Point.N - 2, S256Point.N)
        s = (z + r * self.secret) * k_inv % S256Point.N
        if s > S256Point.N / 2:
            s = S256Point.N - s
        return Signature(r, s)

    def deterministic_k(self, z):
        k = b"\x00" * 32
        v = b"\x01" * 32
        if z > S256Point.N:
            z -= S256Point.N
        z_bytes = z.to_bytes(32, "big")
        secret_bytes = self.secret.to_bytes(32, "big")
        s256 = hashlib.sha256
        k = hmac.new(k, v + b"\x00" + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b"\x01" + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, "big")
            if candidate >= 1 and candidate < S256Point.N:
                return candidate
            k = hmac.new(k, v + b"\x00", s256).digest()
            v = hmac.new(k, v, s256).digest()
