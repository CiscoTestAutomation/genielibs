from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_interface_ospfv3_ipsec_ah


class TestConfigureInterfaceOspfv3IpsecAh(TestCase):

    def test_configure_interface_ospfv3_ipsec_ah(self):
        device = Mock()
        result = configure_interface_ospfv3_ipsec_ah(
            device,
            'TenGigabitEthernet1/0/41',
            25603,
            'md5',
            '1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78',
            None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface TenGigabitEthernet1/0/41', 'ospfv3 authentication ipsec spi 25603 md5 1AAAA2BBBB3CCCC4DDDD5EEEE6FFFF78'],)
        )