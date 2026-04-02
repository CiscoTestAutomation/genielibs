from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import unconfigure_interface_ip_dns_view_group
from unittest.mock import Mock


class TestUnconfigureInterfaceIpDnsViewGroup(TestCase):

    def test_unconfigure_interface_ip_dns_view_group(self):
        self.device = Mock()
        result = unconfigure_interface_ip_dns_view_group(self.device, 'Gigabitethernet0/0', 'test')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Gigabitethernet0/0', 'no ip dns view-group test'],)
        )
