from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ntp.configure import configure_ntp_authenticate
from unittest.mock import Mock


class TestConfigureNtpAuthenticate(TestCase):

    def test_configure_ntp_authenticate(self):
        self.device = Mock()
        result = configure_ntp_authenticate(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ntp authenticate',)
        )
