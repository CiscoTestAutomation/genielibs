from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_crypto_isakmp_profile
from unittest.mock import Mock


class TestConfigureCryptoIsakmpProfile(TestCase):

    def test_configure_crypto_isakmp_profile(self):
        self.device = Mock()
        result = configure_crypto_isakmp_profile(self.device, 'test_isakmp_prof', True, 'rootca', True, 'CERT1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto isakmp profile test_isakmp_prof', 'ca trust-point rootca', 'match certificate CERT1'],)
        )
