from network import NetworkEnvelope, VersionMessage, GetHeadersMessage
import io


class TestNetworkEnvelope:
    def test_parse(self):
        msg = bytes.fromhex("f9beb4d976657261636b000000000000000000005df6e0e2")
        stream = io.BytesIO(msg)
        envelope = NetworkEnvelope.parse(stream)
        assert envelope.command == b"verack"
        assert envelope.payload == b""
        msg = bytes.fromhex(
            "f9beb4d976657273696f6e0000000000650000005f1a69d2721101000100000000000000bc8f5e5400000000010000000000000000000000000000000000ffffc61b6409208d010000000000000000000000000000000000ffffcb0071c0208d128035cbc97953f80f2f5361746f7368693a302e392e332fcf05050001"
        )
        stream = io.BytesIO(msg)
        envelope = NetworkEnvelope.parse(stream)
        assert envelope.command == b"version"
        assert envelope.payload == msg[24:]

    def test_serialize(self):
        msg = bytes.fromhex("f9beb4d976657261636b000000000000000000005df6e0e2")
        stream = io.BytesIO(msg)
        envelope = NetworkEnvelope.parse(stream)
        assert envelope.serialize() == msg
        msg = bytes.fromhex(
            "f9beb4d976657273696f6e0000000000650000005f1a69d2721101000100000000000000bc8f5e5400000000010000000000000000000000000000000000ffffc61b6409208d010000000000000000000000000000000000ffffcb0071c0208d128035cbc97953f80f2f5361746f7368693a302e392e332fcf05050001"
        )
        stream = io.BytesIO(msg)
        envelope = NetworkEnvelope.parse(stream)
        assert envelope.serialize() == msg


class TestVersionMessage:

    def test_serialize(self):
        v = VersionMessage(timestamp=0, nonce=b"\x00" * 8)
        assert (
            v.serialize().hex()
            == "7f11010000000000000000000000000000000000000000000000000000000000000000000000ffff00000000208d000000000000000000000000000000000000ffff00000000208d0000000000000000182f70726f6772616d6d696e67626974636f696e3a302e312f0000000000"
        )


class TestGetHeadersMessage:

    def test_serialize(self):
        block_hex = "0000000000000000001237f46acddf58578a37e213d2a6edc4884a2fcad05ba3"
        gh = GetHeadersMessage(start_block=bytes.fromhex(block_hex))
        assert (
            gh.serialize().hex()
            == "7f11010001a35bd0ca2f4a88c4eda6d213e2378a5758dfcd6af437120000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        )


class HeadersMessageTest:

    def test_parse(self):
        hex_msg = "0200000020df3b053dc46f162a9b00c7f0d5124e2676d47bbe7c5d0793a500000000000000ef445fef2ed495c275892206ca533e7411907971013ab83e3b47bd0d692d14d4dc7c835b67d8001ac157e670000000002030eb2540c41025690160a1014c577061596e32e426b712c7ca00000000000000768b89f07044e6130ead292a3f51951adbd2202df447d98789339937fd006bd44880835b67d8001ade09204600"
        stream = io.BytesIO(bytes.fromhex(hex_msg))
        headers = HeadersMessage.parse(stream)
        self.assertEqual(len(headers.blocks), 2)
        for b in headers.blocks:
            self.assertEqual(b.__class__, Block)
