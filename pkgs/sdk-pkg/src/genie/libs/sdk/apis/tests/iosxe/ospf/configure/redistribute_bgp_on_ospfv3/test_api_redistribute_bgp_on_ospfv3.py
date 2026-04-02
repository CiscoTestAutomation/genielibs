from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import redistribute_bgp_on_ospfv3


class TestRedistributeBgpOnOspfv3(TestCase):

    def test_redistribute_bgp_on_ospfv3(self):
        device = Mock()
        result = redistribute_bgp_on_ospfv3(
            device,
            '30000',
            'ipv6',
            '3000'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'router ospfv3 30000',
                'address-family ipv6 unicast',
                'redistribute bgp 3000',
                'exit-address-family'
            ],)
        )