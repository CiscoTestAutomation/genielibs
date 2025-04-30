from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ntp.configure import configure_ntp_trusted_key
from unittest.mock import Mock


class TestConfigureNtpTrustedKey(TestCase):

    def test_configure_ntp_trusted_key(self):
        self.device = Mock()
        result = configure_ntp_trusted_key(self.device, 1)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ntp trusted-key 1',)
        )
