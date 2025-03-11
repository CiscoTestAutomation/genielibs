from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_database
from unittest.mock import Mock


class TestUnconfigureIpDhcpDatabase(TestCase):

    def test_unconfigure_ip_dhcp_database(self):
        self.device = Mock()
        result = unconfigure_ip_dhcp_database(self.device, 'ftp://user:password@172.16.4.253/router-dhcp')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip dhcp database ftp://user:password@172.16.4.253/router-dhcp',)
        )
