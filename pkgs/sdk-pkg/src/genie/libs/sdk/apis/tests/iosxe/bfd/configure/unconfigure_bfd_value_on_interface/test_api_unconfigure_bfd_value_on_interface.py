from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import unconfigure_bfd_value_on_interface
from unittest.mock import Mock, call


class TestUnconfigureBfdValueOnInterface(TestCase):

    def test_unconfigure_bfd_value_on_interface(self):
        self.device = Mock()
        self.device.configure.return_value = None

        interface_name = 'vlan101'
        bfd_value = 'echo'

        result = unconfigure_bfd_value_on_interface(self.device, interface_name, bfd_value)

        self.device.configure(['interface vlan101', 'no bfd echo'])

        expected_output = None
        self.assertEqual(result, expected_output)