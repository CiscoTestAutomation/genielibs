from unittest import TestCase
from genie.libs.sdk.apis.iosxe.spanning_tree.get import get_configure_spanning_tree_mst_instance_output
from unittest.mock import Mock


class TestGetConfigureSpanningTreeMstInstanceOutput(TestCase):

    def test_get_configure_spanning_tree_mst_instance_output(self):
        self.device = Mock()
        result = get_configure_spanning_tree_mst_instance_output(self.device, '1', '100')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['spanning-tree mst configuration', 'instance 1 vlan 100'],)
        )
