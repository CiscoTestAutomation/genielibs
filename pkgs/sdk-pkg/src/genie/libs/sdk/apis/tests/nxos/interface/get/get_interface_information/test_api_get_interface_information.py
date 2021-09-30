import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.nxos.interface.get import get_interface_information


class TestGetInterfaceInformation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R3_nx:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os nxos --mock_data_dir mock_data --state connect
                protocol: unknown
            os: nxos
            platform: n9kv
            type: NX-OSv 9000
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R3_nx']
        self.device.connect()

    def test_get_interface_information(self):
        result = get_interface_information(self.device, ['mgmt0', 'Loopback0'])
        expected_output = {'mgmt0': {'mgmt0': {'port_channel': {'port_channel_member': False},
                     'link_state': 'up',
                     'oper_status': 'up',
                     'enabled': True,
                     'admin_state': 'up',
                     'types': 'Ethernet',
                     'mac_address': '5e01.4002.0000',
                     'phys_address': '5e01.4002.0000',
                     'ipv4': {'172.16.1.213/24': {'ip': '172.16.1.213',
                                                  'prefix_length': '24'}},
                     'delay': 10,
                     'mtu': 1500,
                     'bandwidth': 1000000,
                     'reliability': '255/255',
                     'txload': '1/255',
                     'rxload': '1/255',
                     'encapsulations': {'encapsulation': 'arpa'},
                     'medium': 'broadcast',
                     'duplex_mode': 'full',
                     'port_speed': '1000',
                     'auto_negotiate': True,
                     'auto_mdix': 'off',
                     'ethertype': '0x0000',
                     'counters': {'rate': {'load_interval': 1,
                                           'in_rate': 184488,
                                           'in_rate_pkts': 136,
                                           'out_rate': 112,
                                           'out_rate_pkts': 0},
                                  'rx': True,
                                  'in_pkts': 112501437,
                                  'in_unicast_pkts': 84826,
                                  'in_multicast_pkts': 111564686,
                                  'in_octets': 11960502,
                                  'in_broadcast_pkts': 3,
                                  'tx': True}}},
 'Loopback0': {'loopback0': {'port_channel': {'port_channel_member': False},
                             'link_state': 'up',
                             'oper_status': 'up',
                             'enabled': True,
                             'admin_state': 'up',
                             'ipv4': {'3.3.3.3/32': {'ip': '3.3.3.3',
                                                     'prefix_length': '32'}},
                             'delay': 5000,
                             'mtu': 1500,
                             'bandwidth': 8000000,
                             'reliability': '255/255',
                             'txload': '1/255',
                             'rxload': '1/255',
                             'encapsulations': {'encapsulation': 'loopback'},
                             'medium': 'broadcast',
                             'auto_mdix': 'off'}}}
        self.assertEqual(result, expected_output)
