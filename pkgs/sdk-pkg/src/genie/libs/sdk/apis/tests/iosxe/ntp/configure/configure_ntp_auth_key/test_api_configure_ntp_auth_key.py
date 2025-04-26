from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ntp.configure import configure_ntp_auth_key
from unittest.mock import Mock


class TestConfigureNtpAuthKey(TestCase):

    def test_configure_ntp_auth_key(self):
        self.device = Mock()
        result = configure_ntp_auth_key(self.device, 1, 'cisco123cisco123', 'cmac-aes-128', 0)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ntp authentication-key 1 cmac-aes-128 cisco123cisco123 0',)
        )
