from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3_redistributed_connected


class TestConfigureOspfv3RedistributedConnected(TestCase):

    def test_configure_ospfv3_redistributed_connected(self):
        device = Mock()
        result = configure_ospfv3_redistributed_connected(
            device,
            '1'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ipv6 router ospf 1', 'redistribute connected'],)
        )