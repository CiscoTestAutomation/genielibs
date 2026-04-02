from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3_ipsec_esp


class TestConfigureOspfv3IpsecEsp(TestCase):

    def test_configure_ospfv3_ipsec_esp(self):
        device = Mock()
        result = configure_ospfv3_ipsec_esp(
            device,
            '1',
            '0',
            25606,
            'aes-cbc',
            '1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78',
            'md5',
            '1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78',
            128,
            None,
            None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'router ospfv3 1',
                'area 0 encryption ipsec spi 25606 esp aes-cbc 128 1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78 md5 1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78'
            ],)
        )