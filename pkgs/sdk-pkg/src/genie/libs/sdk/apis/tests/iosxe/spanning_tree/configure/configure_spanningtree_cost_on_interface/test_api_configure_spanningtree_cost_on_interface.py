from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanningtree_cost_on_interface,
)


class TestConfigureSpanningtreeCostOnInterface(TestCase):

    def test_configure_spanningtree_cost_on_interface(self):
        device = Mock()

        result = configure_spanningtree_cost_on_interface(
            device,
            'GigabitEthernet1/0/3',
            '100'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'interface GigabitEthernet1/0/3',
                    'spanning-tree cost 100',
                ],
            )
        )