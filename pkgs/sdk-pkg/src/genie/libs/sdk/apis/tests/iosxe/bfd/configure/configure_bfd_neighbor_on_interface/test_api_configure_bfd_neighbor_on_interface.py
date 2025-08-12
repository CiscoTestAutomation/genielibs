from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import configure_bfd_neighbor_on_interface
from unittest.mock import Mock, call


class TestConfigureBfdNeighborOnInterface(TestCase):

    def test_configure_bfd_neighbor_on_interface(self):
        self.device = Mock()
        self.device.configure.return_value = None

        interface_name = 'HundredGigE1/0/21'
        address_family = 'ipv6'
        neighbor_ip = '2013:1::20'

        result = configure_bfd_neighbor_on_interface(self.device, interface_name, address_family, neighbor_ip)

        self.device.configure(['interface HundredGigE1/0/21', 'bfd neighbor ipv6 2013:1::20 '])

        expected_output = None
        self.assertEqual(result, expected_output)