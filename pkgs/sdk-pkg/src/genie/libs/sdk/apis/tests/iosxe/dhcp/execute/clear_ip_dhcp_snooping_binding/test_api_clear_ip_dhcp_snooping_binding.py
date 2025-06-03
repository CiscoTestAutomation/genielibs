from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.execute import clear_ip_dhcp_snooping_binding
from unittest.mock import Mock

class TestClearIpDhcpSnoopingBinding(TestCase):

    def test_clear_ip_dhcp_snooping_binding(self):
        self.device = Mock()
        clear_ip_dhcp_snooping_binding(device=self.device)
        self.device.execute.assert_called_with('clear ip dhcp snooping binding *')
