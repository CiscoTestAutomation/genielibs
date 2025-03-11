from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_interface_ipv6_rip
from unittest.mock import Mock


class TestUnconfigureInterfaceIpv6Rip(TestCase):

    def test_unconfigure_interface_ipv6_rip(self):
        self.device = Mock()
        result = unconfigure_interface_ipv6_rip(self.device, 'GigabitEthernet0/0/1', 'test', None, None, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0/1', 'no ipv6 rip test enable'],)
        )
