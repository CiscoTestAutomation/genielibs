from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_eap_profile_advanced
from unittest.mock import Mock


class TestConfigureEapProfileAdvanced(TestCase):

    def test_configure_eap_profile_advanced(self):
        self.device = Mock()
        result = configure_eap_profile_advanced(self.device, 'DUMMY', 'tls', 'tls13-aes256-gcm-sha384', None, None, 'peap', None, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['eap profile DUMMY', 'method tls', 'ciphersuite tls13-aes256-gcm-sha384', 'no method peap'],)
        )
