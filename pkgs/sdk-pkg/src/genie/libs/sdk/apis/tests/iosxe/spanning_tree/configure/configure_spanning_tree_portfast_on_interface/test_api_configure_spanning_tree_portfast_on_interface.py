from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_portfast_on_interface,
)


class TestConfigureSpanningTreePortfastOnInterface(TestCase):

    def test_configure_spanning_tree_portfast_on_interface(self):
        device = Mock()

        result = configure_spanning_tree_portfast_on_interface(
            device,
            'GIgabitEthernet6/0/37',
            None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'interface GIgabitEthernet6/0/37',
                    'spanning-tree portfast',
                ],
            )
        )