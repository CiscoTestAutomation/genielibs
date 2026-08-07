from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_guard_root,
)


class TestUnconfigureSpanningTreeGuardRoot(TestCase):

    def test_unconfigure_spanning_tree_guard_root(self):
        device = Mock()

        result = unconfigure_spanning_tree_guard_root(
            device,
            'TenGigabitEthernet4/1/3'
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface TenGigabitEthernet4/1/3',
                'no spanning-tree guard root',
            ]
        )
