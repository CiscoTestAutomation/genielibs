from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3_address_family


class TestConfigureOspfv3AddressFamily(TestCase):

    def test_configure_ospfv3_address_family(self):
        device = Mock()
        result = configure_ospfv3_address_family(
            device,
            1,
            'ipv6',
            'unicast',
            'connected'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'router ospfv3 1',
                'address-family ipv6 unicast',
                'redistribute connected'
            ],)
        )