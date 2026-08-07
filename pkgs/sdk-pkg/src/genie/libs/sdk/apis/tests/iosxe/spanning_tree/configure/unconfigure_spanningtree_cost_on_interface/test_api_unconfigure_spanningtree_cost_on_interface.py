from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanningtree_cost_on_interface,
)


class TestUnconfigureSpanningtreeCostOnInterface(TestCase):

    def test_unconfigure_spanningtree_cost_on_interface(self):
        device = Mock()

        result = unconfigure_spanningtree_cost_on_interface(
            device,
            'GigabitEthernet1/0/3',
            '100'
        )

        self.assertEqual(result, None)
        device.configure.assert_called_once_with(
            [
                'interface GigabitEthernet1/0/3',
                'no spanning-tree cost 100',
            ]
        )
