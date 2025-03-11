from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_database
from unittest.mock import Mock


class TestConfigureIpDhcpDatabase(TestCase):

    def test_configure_ip_dhcp_database(self):
        self.device = Mock()
        result = configure_ip_dhcp_database(self.device, 'ftp://user:password@172.16.4.253/router-dhcp')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip dhcp database ftp://user:password@172.16.4.253/router-dhcp',)
        )
