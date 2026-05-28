from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rip.configure import unconfigure_rip_auto_summary
from unittest.mock import Mock


class TestUnconfigureRipAutoSummary(TestCase):

    def test_unconfigure_rip_auto_summary(self):
        self.device = Mock()
        result = unconfigure_rip_auto_summary(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router rip', 'no auto-summary'],)
        )
