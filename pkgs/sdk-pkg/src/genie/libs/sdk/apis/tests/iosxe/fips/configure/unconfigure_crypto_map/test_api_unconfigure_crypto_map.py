from unittest import TestCase
from genie.libs.sdk.apis.iosxe.fips.configure import unconfigure_crypto_map
from unittest.mock import Mock


class TestUnconfigureCryptoMap(TestCase):

    def test_unconfigure_crypto_map(self):
        self.device = Mock()
        result = unconfigure_crypto_map(self.device, 'myVpnMap', None, False, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no crypto map myVpnMap'],)
        )
