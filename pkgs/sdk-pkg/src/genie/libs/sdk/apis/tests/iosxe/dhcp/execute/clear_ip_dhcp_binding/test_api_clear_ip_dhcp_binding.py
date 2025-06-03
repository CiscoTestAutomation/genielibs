from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.execute import clear_ip_dhcp_binding
from unittest.mock import Mock

class TestClearIpDhcpBinding(TestCase):

    def test_clear_ip_dhcp_binding(self):
        self.device = Mock()
        clear_ip_dhcp_binding(device=self.device)
        self.device.execute.assert_called_with('clear ip dhcp binding *')

