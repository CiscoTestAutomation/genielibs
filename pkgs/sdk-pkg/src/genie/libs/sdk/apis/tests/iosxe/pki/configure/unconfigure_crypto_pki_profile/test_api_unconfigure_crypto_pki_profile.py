from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import unconfigure_crypto_pki_profile
from unittest.mock import Mock


class TestUnconfigureCryptoPkiProfile(TestCase):

    def test_unconfigure_crypto_pki_profile(self):
        self.device = Mock()
        result = unconfigure_crypto_pki_profile(self.device, 'API_PROF')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no crypto pki profile enrollment API_PROF',)
        )
