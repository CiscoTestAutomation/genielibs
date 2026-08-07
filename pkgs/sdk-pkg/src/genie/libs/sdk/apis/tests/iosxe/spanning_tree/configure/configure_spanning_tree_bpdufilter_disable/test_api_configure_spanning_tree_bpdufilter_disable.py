from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_bpdufilter_disable,
)


class TestConfigureSpanningTreeBpdufilterDisable(TestCase):

    def test_configure_spanning_tree_bpdufilter_disable(self):
        device = Mock()

        result = configure_spanning_tree_bpdufilter_disable(
            device,
            'te1/0/6'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'interface te1/0/6',
                    'spanning-tree bpdufilter disable',
                ],
            )
        )
