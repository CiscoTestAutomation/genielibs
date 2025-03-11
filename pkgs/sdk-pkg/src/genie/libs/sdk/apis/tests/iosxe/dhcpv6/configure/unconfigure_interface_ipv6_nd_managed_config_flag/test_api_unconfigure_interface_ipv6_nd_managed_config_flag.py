from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_interface_ipv6_nd_managed_config_flag
from unittest.mock import Mock


class TestUnconfigureInterfaceIpv6NdManagedConfigFlag(TestCase):

    def test_unconfigure_interface_ipv6_nd_managed_config_flag(self):
        self.device = Mock()
        result = unconfigure_interface_ipv6_nd_managed_config_flag(self.device, 'GigabitEthernet0/0')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface  GigabitEthernet0/0', 'no ipv6 nd managed-config-flag'],)
        )
