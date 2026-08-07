from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_guard_loop,
)


class TestUnconfigureSpanningTreeGuardLoop(TestCase):

    def test_unconfigure_spanning_tree_guard_loop(self):
        device = Mock()

        result = unconfigure_spanning_tree_guard_loop(
            device,
            'TenGigabitEthernet4/1/3'
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface TenGigabitEthernet4/1/3',
                'no spanning-tree guard loop',
            ]
        )
