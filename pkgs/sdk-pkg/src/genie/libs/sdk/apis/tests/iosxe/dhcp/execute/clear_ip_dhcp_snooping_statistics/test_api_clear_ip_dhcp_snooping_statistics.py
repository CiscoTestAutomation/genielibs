from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.execute import clear_ip_dhcp_snooping_statistics
from unittest.mock import Mock

class TestClearIpDhcpSnoopingStatistics(TestCase):

    def test_clear_ip_dhcp_snooping_statistics(self):
        self.device = Mock()
        clear_ip_dhcp_snooping_statistics(self.device)
        self.device.execute.assert_called_with('clear ip dhcp snooping statistics')
