import hashlib

SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

TWO_WEEKS = 60 * 60 * 24 * 14
MAX_TARGET = 0xFFFF * 256 ** (0x1D - 3)


def hash160(s):
    """sha256 followed by ripemd160"""
    return hashlib.new("ripemd160", hashlib.sha256(s).digest()).digest()


def hash256(s):
    """two rounds of sha256"""
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, "big")
    prefix = "1" * count
    result = ""
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result


def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])


def decode_base58(s):
    num = 0
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)
    combined = num.to_bytes(25, byteorder="big")
    checksum = combined[-4:]
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError(
            "bad address: {} {}".format(checksum, hash256(combined[:-4])[:4])
        )
    return combined[1:-4]


def little_endian_to_int(b):
    return int.from_bytes(b, "little")


def int_to_little_endian(n, length):
    return n.to_bytes(length, "little")


def read_varint(s):
    """read_varint reads a variable integer from a stream"""
    i = s.read(1)[0]
    if i == 0xFD:  # 0xfd means the next two bytes are the number
        return little_endian_to_int(s.read(2))
    elif i == 0xFE:  # 0xfe means the next four bytes are the number
        return little_endian_to_int(s.read(4))
    elif i == 0xFF:  # 0xff means the next eight bytes are the number
        return little_endian_to_int(s.read(8))
    else:  # anything else is just the integer
        return i


def encode_varint(i):
    """encodes an integer as a varint"""
    if i < 0xFD:
        return bytes([i])
    elif i < 0x10000:
        return b"\xfd" + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b"\xfe" + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b"\xff" + int_to_little_endian(i, 8)
    else:
        raise ValueError("integer too large: {}".format(i))


def h160_to_p2pkh_address(h160, testnet=False):
    """Takes a byte sequence hash160 and returns a p2pkh address string"""
    # p2pkh has a prefix of b'\x00' for mainnet, b'\x6f' for testnet
    if testnet:
        prefix = b"\x6f"
    else:
        prefix = b"\x00"
    return encode_base58_checksum(prefix + h160)


def h160_to_p2sh_address(h160, testnet=False):
    """Takes a byte sequence hash160 and returns a p2sh address string"""
    # p2sh has a prefix of b'\x05' for mainnet, b'\xc4' for testnet
    if testnet:
        prefix = b"\xc4"
    else:
        prefix = b"\x05"
    return encode_base58_checksum(prefix + h160)


def bits_to_target(bits):
    """Turns bits into a target (large 256-bit integer)"""
    # last byte is exponent
    exponent = bits[-1]
    # the first three bytes are the coefficient in little endian
    coefficient = little_endian_to_int(bits[:-1])
    # the formula is:
    # coefficient * 256**(exponent-3)
    return coefficient * 256 ** (exponent - 3)


def target_to_bits(target):
    """Turns a target integer back into bits"""
    raw_bytes = target.to_bytes(32, "big")
    raw_bytes = raw_bytes.lstrip(b"\x00")  # <1>
    if raw_bytes[0] > 0x7F:  # <2>
        exponent = len(raw_bytes) + 1
        coefficient = b"\x00" + raw_bytes[:2]
    else:
        exponent = len(raw_bytes)  # <3>
        coefficient = raw_bytes[:3]  # <4>
    new_bits = coefficient[::-1] + bytes([exponent])  # <5>
    return new_bits


def calculate_new_bits(previous_bits, time_differential):
    """Calculates the new bits given
    a 2016-block time differential and the previous bits"""
    # if the time differential is greater than 8 weeks, set to 8 weeks
    if time_differential > TWO_WEEKS * 4:
        time_differential = TWO_WEEKS * 4
    # if the time differential is less than half a week, set to half a week
    if time_differential < TWO_WEEKS // 4:
        time_differential = TWO_WEEKS // 4
    # the new target is the previous target * time differential / two weeks
    new_target = bits_to_target(previous_bits) * time_differential // TWO_WEEKS
    # if the new target is bigger than MAX_TARGET, set to MAX_TARGET
    if new_target > MAX_TARGET:
        new_target = MAX_TARGET
    # convert the new target to bits
    return target_to_bits(new_target)
