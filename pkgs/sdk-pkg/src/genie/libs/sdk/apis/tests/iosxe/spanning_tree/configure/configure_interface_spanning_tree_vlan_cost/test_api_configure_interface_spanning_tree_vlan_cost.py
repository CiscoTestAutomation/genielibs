from unittest import TestCase
from genie.libs.sdk.apis.iosxe.spanning_tree.configure import \
    configure_interface_spanning_tree_vlan_cost
from unittest.mock import Mock


class TestConfigureInterfaceSpanningTreeVlanCost(TestCase):

    def test_configure_interface_spanning_tree_vlan_cost(self):
        self.device = Mock()
        result = configure_interface_spanning_tree_vlan_cost(
            self.device, 'GigabitEthernet0/1/1', '100', '8'
        )
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/1/1',
              'spanning-tree vlan 100 cost 8'],)
        )
