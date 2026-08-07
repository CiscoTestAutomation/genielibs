from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanningtree_sso_block_tcn,
)


class TestConfigureSpanningtreeSsoBlockTcn(TestCase):

    def test_configure_spanningtree_sso_block_tcn(self):
        device = Mock()

        result = configure_spanningtree_sso_block_tcn(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['spanning-tree sso block-tcn'],)
        )