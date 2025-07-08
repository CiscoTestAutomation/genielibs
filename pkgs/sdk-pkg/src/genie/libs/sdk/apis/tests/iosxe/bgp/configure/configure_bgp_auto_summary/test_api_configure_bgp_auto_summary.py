from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_auto_summary
from unittest.mock import Mock 

class TestConfigureBgpAutoSummary(TestCase):

    def test_configure_bgp_auto_summary(self):
        self.device = Mock()
        configure_bgp_auto_summary(self.device, '100')
        self.device.configure.assert_called_with(['router bgp 100', 'auto-summary'])
