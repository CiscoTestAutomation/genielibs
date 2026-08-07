from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_priority,
)


class TestConfigureSpanningTreePriority(TestCase):

    def test_configure_spanning_tree_priority(self):
        device = Mock()

        result = configure_spanning_tree_priority(
            device,
            '123',
            '4096'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'spanning-tree vlan 123 priority 4096',
            )
        )