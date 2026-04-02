from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3_on_interface


class TestConfigureOspfv3OnInterface(TestCase):

    def test_configure_ospfv3_on_interface(self):
        device = Mock()
        result = configure_ospfv3_on_interface(
            device,
            'TwentyFiveGigE1/0/2',
            '100',
            0
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface TwentyFiveGigE1/0/2', 'ospfv3 100 area 0 ipv6'],)
        )