from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_uplinkfast,
)


class TestConfigureSpanningTreeUplinkfast(TestCase):

    def test_configure_spanning_tree_uplinkfast(self):
        device = Mock()

        result = configure_spanning_tree_uplinkfast(
            device,
            555
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'spanning-tree uplinkfast max-update-rate 555',
            )
        )