from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_mode,
)


class TestConfigureSpanningTreeMode(TestCase):

    def test_configure_spanning_tree_mode(self):
        device = Mock()

        result = configure_spanning_tree_mode(
            device,
            'pvst',
            'extend system-id'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'spanning-tree mode pvst',
                    'spanning-tree extend system-id',
                ],
            )
        )
