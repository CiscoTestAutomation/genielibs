from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cdp.configure import configure_cdp_log_mismatch_duplex
from unittest.mock import Mock


class TestConfigureCdpLogMismatchDuplex(TestCase):

    def test_configure_cdp_log_mismatch_duplex(self):
        self.device = Mock()
        result = configure_cdp_log_mismatch_duplex(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['cdp log mismatch duplex'],)
        )
