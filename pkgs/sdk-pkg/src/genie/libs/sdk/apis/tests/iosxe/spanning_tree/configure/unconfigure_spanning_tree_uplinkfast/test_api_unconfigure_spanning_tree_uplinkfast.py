from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_uplinkfast,
)


class TestUnconfigureSpanningTreeUplinkfast(TestCase):

    def test_unconfigure_spanning_tree_uplinkfast(self):
        device = Mock()

        result = unconfigure_spanning_tree_uplinkfast(
            device,
            555
        )

        self.assertEqual(result, None)
        device.configure.assert_called_once_with(
            'no spanning-tree uplinkfast max-update-rate'
        )
