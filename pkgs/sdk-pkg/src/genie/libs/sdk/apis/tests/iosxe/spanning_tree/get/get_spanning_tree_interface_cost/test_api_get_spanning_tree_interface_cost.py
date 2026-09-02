from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.get import get_spanning_tree_interface_cost


class TestGetSpanningTreeInterfaceCost(TestCase):
    def test_get_spanning_tree_interface_cost(self):
        device = Mock()
        device.parse.return_value = {
            'vlan': {
                'G0:VLAN0100': {
                    'cost': 20000
                }
            }
        }

        result = get_spanning_tree_interface_cost(
            device, '100', 'GigabitEthernet0/1/0')

        device.parse.assert_called_once_with(
            'show spanning-tree interface GigabitEthernet0/1/0')
        self.assertEqual(20000, result)
