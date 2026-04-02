from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import configure_interface_ip_dns_view_group
from unittest.mock import Mock


class TestConfigureInterfaceIpDnsViewGroup(TestCase):

    def test_configure_interface_ip_dns_view_group(self):
        self.device = Mock()
        result = configure_interface_ip_dns_view_group(self.device, 'Gigabitethernet0/0', 'test')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Gigabitethernet0/0', 'ip dns view-group test'],)
        )
