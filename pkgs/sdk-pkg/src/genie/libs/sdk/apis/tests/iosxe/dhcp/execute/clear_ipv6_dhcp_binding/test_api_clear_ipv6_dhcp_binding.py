from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.execute import clear_ipv6_dhcp_binding
from unittest.mock import Mock

class TestClearIpv6DhcpBinding(TestCase):

    def test_clear_ipv6_dhcp_binding(self):
        self.device = Mock()
        clear_ipv6_dhcp_binding(self.device)
        self.device.execute.assert_called_with('clear ipv6 dhcp binding *')
