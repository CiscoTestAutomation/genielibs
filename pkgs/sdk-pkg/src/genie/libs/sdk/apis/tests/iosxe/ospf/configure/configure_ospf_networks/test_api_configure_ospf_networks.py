from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_networks


class TestConfigureOspfNetworks(TestCase):

    def test_configure_ospf_networks(self):
        device = Mock()
        result = configure_ospf_networks(
            device,
            10,
            ['172.16.70.0', '172.16.71.0', '172.16.80.0'],
            '0.0.0.255',
            0,
            '1.1.1.1',
            'all-interfaces',
            'green'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 10 vrf green','network 172.16.70.0 0.0.0.255 area 0','network 172.16.71.0 0.0.0.255 area 0','network 172.16.80.0 0.0.0.255 area 0','router-id 1.1.1.1','bfd all-interfaces'],)
        )

    def test_configure_ospf_networks_1(self):
        device = Mock()
        result = configure_ospf_networks(
            device,
            9,
            ['172.16.70.0', '172.16.71.0', '172.16.80.0'],
            '0.0.0.255',
            0,
            '1.1.1.1',
            'all-interfaces',
            None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 9','network 172.16.70.0 0.0.0.255 area 0','network 172.16.71.0 0.0.0.255 area 0','network 172.16.80.0 0.0.0.255 area 0','router-id 1.1.1.1','bfd all-interfaces'],)
        )

    def test_configure_ospf_networks_2(self):
        device = Mock()
        result = configure_ospf_networks(
            device,
            5,
            None,
            None,
            None,
            '1.1.1.1',
            'all-interfaces',
            'green'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 5 vrf green', 'router-id 1.1.1.1', 'bfd all-interfaces'],)
        )