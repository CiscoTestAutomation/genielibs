from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3


class TestConfigureOspfv3(TestCase):

    def test_configure_ospfv3(self):
        device = Mock()
        result = configure_ospfv3(
            device,
            '1',
            '1.1.1.1',
            None,
            True,
            True,
            'ipv4',
            None,
            None,
            None,
            True,
            'connected',
            0,
            1
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'router ospfv3 1',
                'graceful-restart',
                'nsr',
                'address-family ipv4',
                'router-id 1.1.1.1',
                'redistribute connected',
                'exit-address-family'
            ],)
        )

    def test_configure_ospfv3_1(self):
        device = Mock()
        result = configure_ospfv3(
            device,
            '1',
            '1.1.1.1',
            None,
            True,
            True,
            'ipv4',
            None,
            'unicast',
            None,
            True,
            'connected',
            1,
            1
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'router ospfv3 1',
                'graceful-restart',
                'nsr',
                'address-family ipv4 unicast',
                'router-id 1.1.1.1',
                'redistribute connected metric 1 metric-type 1',
                'exit-address-family'
            ],)
        )