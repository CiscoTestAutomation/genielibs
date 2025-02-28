from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_eap_profile
from unittest.mock import Mock


class TestConfigureEapProfile(TestCase):

    def test_configure_eap_profile(self):
        self.device = Mock()
        result = configure_eap_profile(self.device, 'eap_fast', 'md5', 'aes128-sha')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('eap profile eap_fast\nmethod md5\nciphersuite aes128-sha\n',)
        )
