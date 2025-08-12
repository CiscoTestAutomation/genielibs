from unittest import TestCase
from genie.libs.sdk.apis.iosxe.fips.configure import unconfigure_crypto_map_xauthmap
from unittest.mock import Mock


class TestUnconfigureCryptoMapXauthmap(TestCase):

    def test_unconfigure_crypto_map_xauthmap(self):
        self.device = Mock()
        result = unconfigure_crypto_map_xauthmap(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no crypto map xauthmap'],)
        )
