from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_interface_ip_ddns_update
from unittest.mock import Mock


class TestConfigureInterfaceIpDdnsUpdate(TestCase):

    def test_configure_interface_ip_ddns_update(self):
        self.device = Mock()
        result = configure_interface_ip_ddns_update(self.device, 'GigabitEthernet1/0/8', 'myupdate', False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/8', 'ip ddns update myupdate'],)
        )
