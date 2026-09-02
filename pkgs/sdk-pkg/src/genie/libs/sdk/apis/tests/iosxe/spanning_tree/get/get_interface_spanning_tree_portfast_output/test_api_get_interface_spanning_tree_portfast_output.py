from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.get import get_interface_spanning_tree_portfast_output


class TestGetInterfaceSpanningTreePortfastOutput(TestCase):
    def test_get_interface_spanning_tree_portfast_output(self):
        device = Mock()
        expected_output = (
            "%Warning: portfast should only be enabled on ports connected to a single\r\n"
            " host. Connecting hubs, concentrators, switches, bridges, etc... to this\r\n"
            " interface  when portfast is enabled, can cause temporary bridging loops.\r\n"
            " Use with CAUTION\r\n\r\n"
            "%Portfast has been configured on GigabitEthernet0/1/0 but will only\r\n"
            " have effect when the interface is in a non-trunking mode.\r\n"
        )
        device.config.return_value = expected_output

        result = get_interface_spanning_tree_portfast_output(
            device, 'GigabitEthernet0/1/0')

        device.config.assert_called_once_with(
            ['interface GigabitEthernet0/1/0', 'spanning-tree portfast'])
        self.assertEqual(expected_output, result)
        self.assertIn('%Warning:', result)
