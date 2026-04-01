from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_network_non_broadcast


class TestConfigureOspfNetworkNonBroadcast(TestCase):

    def test_configure_ospf_network_non_broadcast(self):
        device = Mock()
        result = configure_ospf_network_non_broadcast(
            device,
            'tunnel1'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface tunnel1', 'ip ospf network non-broadcast'],)
        )