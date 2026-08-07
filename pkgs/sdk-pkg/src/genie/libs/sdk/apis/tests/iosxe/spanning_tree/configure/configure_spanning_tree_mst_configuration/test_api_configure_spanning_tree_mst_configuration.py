from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_mst_configuration,
)


class TestConfigureSpanningTreeMstConfiguration(TestCase):

    def test_configure_spanning_tree_mst_configuration(self):
        device = Mock()

        result = configure_spanning_tree_mst_configuration(
            device,
            1,
            2,
            102
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['spanning-tree mst configuration', 'instance 1 vlan 2, 102'],)
        )
