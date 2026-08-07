from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_portfast_on_interface,
)


class TestUnconfigureSpanningTreePortfastOnInterface(TestCase):

    def test_unconfigure_spanning_tree_portfast_on_interface(self):
        device = Mock()

        result = unconfigure_spanning_tree_portfast_on_interface(
            device,
            'TwoGigabitEthernet8/0/25',
            None
        )

        self.assertEqual(result, None)
        device.configure.assert_called_once_with(
            [
                'interface TwoGigabitEthernet8/0/25',
                'no spanning-tree portfast',
            ]
        )
