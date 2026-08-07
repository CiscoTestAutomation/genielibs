from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_default_spanning_tree,
)


class TestConfigureDefaultSpanningTree(TestCase):

    def test_configure_default_spanning_tree(self):
        device = Mock()

        result = configure_default_spanning_tree(
            device,
            'etherchannel guard misconfig',
            '',
            '',
            ''
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'default spanning-tree etherchannel guard misconfig',
            )
        )
