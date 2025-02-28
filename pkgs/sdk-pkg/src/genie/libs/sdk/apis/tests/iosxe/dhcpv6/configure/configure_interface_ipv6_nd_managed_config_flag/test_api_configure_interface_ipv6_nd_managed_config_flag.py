from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_interface_ipv6_nd_managed_config_flag
from unittest.mock import Mock


class TestConfigureInterfaceIpv6NdManagedConfigFlag(TestCase):

    def test_configure_interface_ipv6_nd_managed_config_flag(self):
        self.device = Mock()
        result = configure_interface_ipv6_nd_managed_config_flag(self.device, 'GigabitEthernet0/0')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface  GigabitEthernet0/0', 'ipv6 nd managed-config-flag'],)
        )
