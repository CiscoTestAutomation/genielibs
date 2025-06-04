from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.utils import clear_dhcpv4_server_stats
from unittest.mock import Mock

class TestClearDHCPv4ServerStats(TestCase):

    def test_clear_dhcpv4_server_stats(self):
        self.device = Mock()
        clear_dhcpv4_server_stats(device=self.device)
        self.device.execute.assert_called_with('clear ip dhcp server statistics')


        
