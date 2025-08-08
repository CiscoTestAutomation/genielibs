from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import unconfigure_bfd_on_interface
from unittest.mock import Mock, call


class TestUnconfigureBfdOnInterface(TestCase):

    def test_unconfigure_bfd_on_interface(self):
        self.device = Mock()
        self.device.configure.return_value = None

        interface_name = 'HundredGigE1/0/21'

        result = unconfigure_bfd_on_interface(device=self.device, interface=interface_name)

        self.device.configure(['interface HundredGigE1/0/21', 'no bfd interval'])

        expected_output = None
        self.assertEqual(result, expected_output)