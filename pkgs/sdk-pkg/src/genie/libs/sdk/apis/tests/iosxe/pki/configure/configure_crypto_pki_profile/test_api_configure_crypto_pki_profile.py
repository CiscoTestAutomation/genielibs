from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_crypto_pki_profile
from unittest.mock import Mock


class TestConfigureCryptoPkiProfile(TestCase):

    def test_configure_crypto_pki_profile(self):
        self.device = Mock()
        result = configure_crypto_pki_profile(self.device, 'API_PROF', True, 'ashrishe', '0', 'nopassword', 'https://10.106.29.252:443', 'GigabitEthernet2', None, None, None, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto pki profile enrollment API_PROF', 'method-est', 'enrollment http username ashrishe password 0 nopassword', 'enrollment url https://10.106.29.252:443', 'source-interface GigabitEthernet2'],)
        )
