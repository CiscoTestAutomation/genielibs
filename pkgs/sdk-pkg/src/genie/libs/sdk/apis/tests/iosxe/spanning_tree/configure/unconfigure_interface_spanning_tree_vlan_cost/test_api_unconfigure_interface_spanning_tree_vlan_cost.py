from unittest import TestCase
from genie.libs.sdk.apis.iosxe.spanning_tree.configure import \
    unconfigure_interface_spanning_tree_vlan_cost
from unittest.mock import Mock


class TestUnconfigureInterfaceSpanningTreeVlanCost(TestCase):

    def test_unconfigure_interface_spanning_tree_vlan_cost(self):
        self.device = Mock()
        result = unconfigure_interface_spanning_tree_vlan_cost(
            self.device, 'GigabitEthernet0/1/1', '100'
        )
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/1/1',
              'no spanning-tree vlan 100 cost'],)
        )
