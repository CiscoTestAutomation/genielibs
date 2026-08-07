from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_guard_root,
)


class TestConfigureSpanningTreeGuardRoot(TestCase):

    def test_configure_spanning_tree_guard_root(self):
        device = Mock()

        result = configure_spanning_tree_guard_root(
            device,
            'TenGigabitEthernet4/1/3'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'interface TenGigabitEthernet4/1/3',
                    'spanning-tree guard root',
                ],
            )
        )
