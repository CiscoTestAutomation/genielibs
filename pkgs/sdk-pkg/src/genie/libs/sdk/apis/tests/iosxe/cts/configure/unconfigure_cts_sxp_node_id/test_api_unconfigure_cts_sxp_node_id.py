from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_sxp_node_id
from unittest.mock import Mock


class TestUnconfigureCtsSxpNodeId(TestCase):

    def test_unconfigure_cts_sxp_node_id(self):
        self.device = Mock()
        result = unconfigure_cts_sxp_node_id(self.device, 'ipv6', '1144:1:1::1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no cts sxp node-id ipv6 1144:1:1::1',)
        )
