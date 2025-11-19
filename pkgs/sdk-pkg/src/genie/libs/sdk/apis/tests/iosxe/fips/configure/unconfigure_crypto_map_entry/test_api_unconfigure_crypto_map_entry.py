from unittest import TestCase
from genie.libs.sdk.apis.iosxe.fips.configure import unconfigure_crypto_map_entry
from unittest.mock import Mock


class TestUnconfigureCryptoMapEntry(TestCase):

    def test_unconfigure_crypto_map_entry(self):
        self.device = Mock()
        result = unconfigure_crypto_map_entry(self.device, 'ikev2-cryptomap', '1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no crypto map ikev2-cryptomap 1'],)
        )
