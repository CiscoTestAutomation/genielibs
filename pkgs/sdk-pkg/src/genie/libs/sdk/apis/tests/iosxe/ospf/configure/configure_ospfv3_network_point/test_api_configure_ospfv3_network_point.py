from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3_network_point


class TestConfigureOspfv3NetworkPoint(TestCase):

    def test_configure_ospfv3_network_point(self):
        device = Mock()
        result = configure_ospfv3_network_point(
            device=device,
            interface='HundredGigE1/0/21'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface HundredGigE1/0/21', 'ipv6 ospf network point-to-point'],)
        )