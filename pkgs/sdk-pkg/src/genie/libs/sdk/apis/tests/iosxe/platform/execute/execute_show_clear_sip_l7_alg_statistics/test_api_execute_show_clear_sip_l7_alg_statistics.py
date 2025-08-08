from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_show_clear_sip_l7_alg_statistics
from unittest.mock import Mock

class TestShowPlatformHardwareQfpActiveFeatureAlgSipL7DataClear(TestCase):

    def test_clear_ip_dhcp_binding(self):
        self.device = Mock()
        execute_show_clear_sip_l7_alg_statistics(device=self.device)
        self.device.execute.assert_called_with('show platform hardware qfp active feature alg statistics sip l7data clear')