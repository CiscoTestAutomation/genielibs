from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanningtree_sso_block_tcn,
)


class TestUnconfigureSpanningtreeSsoBlockTcn(TestCase):

    def test_unconfigure_spanningtree_sso_block_tcn(self):
        device = Mock()

        result = unconfigure_spanningtree_sso_block_tcn(device)

        self.assertEqual(result, None)
        device.configure.assert_called_once_with(
            ['no spanning-tree sso block-tcn']
        )
