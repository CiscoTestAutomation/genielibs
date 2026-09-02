from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.get import get_show_spanning_tree_interface_detail_output


class TestGetShowSpanningTreeInterfaceDetailOutput(TestCase):
    def test_get_show_spanning_tree_interface_detail_output(self):
        device = Mock()
        expected_output = {
            'port': 7,
            'interface': 'GigabitEthernet0/1/0',
            'vlan': 'VLAN0100',
            'role': 'root',
            'status': 'forwarding',
            'BPDU': {
                'sent': 1,
                'received': 1692899
            }
        }
        device.parse.return_value = expected_output

        result = get_show_spanning_tree_interface_detail_output(
            device, 'GigabitEthernet0/1/0')

        device.parse.assert_called_once_with(
            'show spanning-tree interface GigabitEthernet0/1/0 detail')
        self.assertEqual(expected_output, result)
        self.assertIsNotNone(result)
        self.assertIn('BPDU', result.keys())
