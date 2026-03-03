from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_sxp_node_id
from unittest.mock import Mock


class TestConfigureCtsSxpNodeId(TestCase):

    def test_configure_cts_sxp_node_id(self):
        self.device = Mock()
        result = configure_cts_sxp_node_id(self.device, 'ipv6', '1144:1:1::1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('cts sxp node-id ipv6 1144:1:1::1',)
        )
