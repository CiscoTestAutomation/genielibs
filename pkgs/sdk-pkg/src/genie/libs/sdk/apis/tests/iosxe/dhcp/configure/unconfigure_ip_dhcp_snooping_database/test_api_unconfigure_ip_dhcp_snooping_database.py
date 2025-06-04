from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_snooping_database
from unittest.mock import Mock


class TestUnconfigureIpDhcpSnoopingDatabase(TestCase):
    def test_unconfigure_ip_dhcp_snooping_database(self):
        self.device = Mock()
        unconfigure_ip_dhcp_snooping_database(self.device, 'bootflash:dhcpsnoop.db', False, '10')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip dhcp snooping database bootflash:dhcpsnoop.db'],))
        
