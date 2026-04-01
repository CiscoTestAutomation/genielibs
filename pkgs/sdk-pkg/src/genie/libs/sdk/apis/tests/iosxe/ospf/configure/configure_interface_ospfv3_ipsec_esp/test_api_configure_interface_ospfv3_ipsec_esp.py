from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_interface_ospfv3_ipsec_esp


class TestConfigureInterfaceOspfv3IpsecEsp(TestCase):

    def test_configure_interface_ospfv3_ipsec_esp(self):
        device = Mock()
        result = configure_interface_ospfv3_ipsec_esp(
            device,
            'TenGigabitEthernet1/0/41',
            25604,
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
            (['interface TenGigabitEthernet1/0/41', 'ospfv3 encryption ipsec spi 25604 esp aes-cbc 128 1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78 md5 1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78'],)
        )