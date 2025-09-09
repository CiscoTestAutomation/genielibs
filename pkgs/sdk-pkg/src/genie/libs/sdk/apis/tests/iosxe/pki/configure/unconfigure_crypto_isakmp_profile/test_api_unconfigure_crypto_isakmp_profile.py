from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import unconfigure_crypto_isakmp_profile
from unittest.mock import Mock


class TestUnconfigureCryptoIsakmpProfile(TestCase):

    def test_unconfigure_crypto_isakmp_profile(self):
        self.device = Mock()
        result = unconfigure_crypto_isakmp_profile(self.device, 'test_isakmp_prof')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no crypto isakmp profile test_isakmp_prof'],)
        )
