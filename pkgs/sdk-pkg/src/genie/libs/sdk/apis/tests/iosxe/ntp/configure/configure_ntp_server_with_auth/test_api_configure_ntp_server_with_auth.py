from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ntp.configure import configure_ntp_server_with_auth
from unittest.mock import Mock


class TestConfigureNtpServerWithAuth(TestCase):

    def test_configure_ntp_server_with_auth(self):
        self.device = Mock()
        result = configure_ntp_server_with_auth(self.device, '1.1.1.1', 1, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ntp server 1.1.1.1 key 1',)
        )
