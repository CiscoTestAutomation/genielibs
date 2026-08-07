from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_default_spanning_tree_mode,
)


class TestConfigureDefaultSpanningTreeMode(TestCase):

    def test_configure_default_spanning_tree_mode(self):
        device = Mock()

        result = configure_default_spanning_tree_mode(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'default spanning-tree mode',
            )
        )
