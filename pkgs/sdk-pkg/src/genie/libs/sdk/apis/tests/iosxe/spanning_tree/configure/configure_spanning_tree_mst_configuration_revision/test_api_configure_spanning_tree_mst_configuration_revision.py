from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_mst_configuration_revision,
)


class TestConfigureSpanningTreeMstConfigurationRevision(TestCase):

    def test_configure_spanning_tree_mst_configuration_revision(self):
        device = Mock()

        result = configure_spanning_tree_mst_configuration_revision(
            device,
            5
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'spanning-tree mst configuration',
                    'revision 5',
                ],
            )
        )
