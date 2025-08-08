from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import enable_bfd_on_isis_ipv6_address
from unittest.mock import Mock, call


class TestEnableBfdOnIsisIpv6Address(TestCase):

    def test_enable_bfd_on_isis_ipv6_address(self):
        self.device = Mock()
        self.device.configure.return_value = None

        interface_name = 'vlan101'

        result = enable_bfd_on_isis_ipv6_address(self.device, interface_name)

        self.device.configure(['interface vlan101', 'isis ipv6 bfd'])

        expected_output = None
        self.assertEqual(result, expected_output)