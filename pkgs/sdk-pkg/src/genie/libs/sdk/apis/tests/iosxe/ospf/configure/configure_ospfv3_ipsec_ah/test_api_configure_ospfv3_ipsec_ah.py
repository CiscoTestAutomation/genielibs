from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3_ipsec_ah


class TestConfigureOspfv3IpsecAh(TestCase):

    def test_configure_ospfv3_ipsec_ah(self):
        device = Mock()
        result = configure_ospfv3_ipsec_ah(
            device,
            '1',
            '0',
            25605,
            'md5',
            '1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78',
            None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'router ospfv3 1',
                'area 0 authentication ipsec spi 25605 md5 1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78'
            ],)
        )