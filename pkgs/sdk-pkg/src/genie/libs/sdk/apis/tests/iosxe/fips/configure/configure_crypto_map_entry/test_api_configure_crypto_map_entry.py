from unittest import TestCase
from genie.libs.sdk.apis.iosxe.fips.configure import configure_crypto_map_entry
from unittest.mock import Mock


class TestConfigureCryptoMapEntry(TestCase):

    def test_configure_crypto_map_entry(self):
        self.device = Mock()
        result = configure_crypto_map_entry(self.device, 'ikev2-cryptomap', '1', '172.20.249.12', 'aes256-sha1', 'ikev2profile', '102', 'ipsec-isakmp', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto map ikev2-cryptomap 1 ipsec-isakmp', 'set peer 172.20.249.12', 'set transform-set aes256-sha1', 'set ikev2-profile ikev2profile', 'match address 102'],)
        )
