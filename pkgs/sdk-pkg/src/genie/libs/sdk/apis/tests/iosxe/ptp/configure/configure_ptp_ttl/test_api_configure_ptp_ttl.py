from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ptp.configure import configure_ptp_ttl
from unittest.mock import Mock


class TestConfigurePtpTtl(TestCase):

    def test_configure_ptp_ttl(self):
        self.device = Mock()
        result = configure_ptp_ttl(self.device, '2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ptp ttl 2'],)
        )
