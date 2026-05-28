from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rip.configure import configure_rip_auto_summary
from unittest.mock import Mock


class TestConfigureRipAutoSummary(TestCase):

    def test_configure_rip_auto_summary(self):
        self.device = Mock()
        result = configure_rip_auto_summary(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router rip', 'auto-summary'],)
        )
