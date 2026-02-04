from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cdp.configure import unconfigure_cdp_log_mismatch_duplex
from unittest.mock import Mock


class TestUnconfigureCdpLogMismatchDuplex(TestCase):

    def test_unconfigure_cdp_log_mismatch_duplex(self):
        self.device = Mock()
        result = unconfigure_cdp_log_mismatch_duplex(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cdp log mismatch duplex'],)
        )
