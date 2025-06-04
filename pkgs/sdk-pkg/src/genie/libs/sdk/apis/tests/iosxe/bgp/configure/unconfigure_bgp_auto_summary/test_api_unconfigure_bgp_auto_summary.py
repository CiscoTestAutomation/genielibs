from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_bgp_auto_summary
from unittest.mock import Mock


class TestUnconfigureBgpAutoSummary(TestCase):

    def test_unconfigure_bgp_auto_summary(self):
        self.device = Mock()
        result = unconfigure_bgp_auto_summary(self.device, '100')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 100', 'no auto-summary'],)
        )
