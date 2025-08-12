from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import disable_bfd_on_isis_ipv6_address
from unittest.mock import Mock, call


class TestDisableBfdOnIsisIpv6Address(TestCase):

    def test_disable_bfd_on_isis_ipv6_address(self):
        self.device = Mock()
        self.device.configure.return_value = None

        interface_name = 'vlan101'

        result = disable_bfd_on_isis_ipv6_address(self.device, interface_name)

        self.device.configureconfigure(['interface vlan101', 'no isis ipv6 bfd'])

        expected_output = None
        self.assertEqual(result, expected_output)