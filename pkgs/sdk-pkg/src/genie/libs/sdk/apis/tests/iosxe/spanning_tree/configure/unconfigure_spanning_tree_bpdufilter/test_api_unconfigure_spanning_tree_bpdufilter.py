from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_bpdufilter,
)


class TestUnconfigureSpanningTreeBpdufilter(TestCase):

    def test_unconfigure_spanning_tree_bpdufilter(self):
        device = Mock()

        result = unconfigure_spanning_tree_bpdufilter(
            device,
            'FortyGigabitEthernet2/0/9'
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ['interface FortyGigabitEthernet2/0/9', 'no spanning-tree bpdufilter']
        )
