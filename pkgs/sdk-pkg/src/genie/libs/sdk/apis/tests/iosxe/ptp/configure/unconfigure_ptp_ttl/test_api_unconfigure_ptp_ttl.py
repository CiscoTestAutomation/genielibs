from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ptp.configure import unconfigure_ptp_ttl
from unittest.mock import Mock


class TestUnconfigurePtpTtl(TestCase):

    def test_unconfigure_ptp_ttl(self):
        self.device = Mock()
        result = unconfigure_ptp_ttl(self.device, '2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ptp ttl 2'],)
        )
