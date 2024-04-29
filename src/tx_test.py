from tx import Tx
import io


class TestTx:
    def test_parse(self):
        tx_stream = io.BytesIO(bytearray.fromhex("01000000"))
        tx = Tx.parse(tx_stream)
        assert tx.version == 1
