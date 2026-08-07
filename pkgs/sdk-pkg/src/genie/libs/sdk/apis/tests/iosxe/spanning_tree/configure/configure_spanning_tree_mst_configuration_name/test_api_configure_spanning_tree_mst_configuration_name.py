from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_mst_configuration_name,
)


class TestConfigureSpanningTreeMstConfigurationName(TestCase):

    def test_configure_spanning_tree_mst_configuration_name(self):
        device = Mock()

        result = configure_spanning_tree_mst_configuration_name(
            device,
            'cisco'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'spanning-tree mst configuration',
                    'name cisco',
                ],
            )
        )
