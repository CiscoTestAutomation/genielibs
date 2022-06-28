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
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_interface_information(self):
        result = get_interface_information(device=self.device, interface_list=['mgmt0', 'Loopback0'])
        expected_output = {'Loopback0': {'loopback0': {'admin_state': 'up',
                             'auto_mdix': 'off',
                             'bandwidth': 8000000,
                             'delay': 5000,
                             'enabled': True,
                             'encapsulations': {'encapsulation': 'loopback'},
                             'ipv4': {'3.3.3.3/32': {'ip': '3.3.3.3',
                                                     'prefix_length': '32'}},
                             'link_state': 'up',
                             'medium': 'broadcast',
                             'mtu': 1500,
                             'oper_status': 'up',
                             'port_channel': {'port_channel_member': False},
                             'reliability': '255/255',
                             'rxload': '1/255',
                             'txload': '1/255'}},
 'mgmt0': {'mgmt0': {'admin_state': 'up',
                     'auto_mdix': 'off',
                     'auto_negotiate': True,
                     'bandwidth': 1000000,
                     'counters': {'in_broadcast_pkts': 3,
                                  'in_multicast_pkts': 360263430,
                                  'in_octets': 35486383,
                                  'in_pkts': 362641345,
                                  'in_unicast_pkts': 251829,
                                  'rate': {'in_rate': 175296,
                                           'in_rate_pkts': 130,
                                           'load_interval': 1,
                                           'out_rate': 120,
                                           'out_rate_pkts': 0},
                                  'rx': True,
                                  'tx': True},
                     'delay': 10,
                     'duplex_mode': 'full',
                     'enabled': True,
                     'encapsulations': {'encapsulation': 'arpa'},
                     'ethertype': '0x0000',
                     'ipv4': {'172.16.1.54/24': {'ip': '172.16.1.54',
                                                 'prefix_length': '24'}},
                     'link_state': 'up',
                     'mac_address': '5e03.8002.0000',
                     'medium': 'broadcast',
                     'mtu': 1500,
                     'oper_status': 'up',
                     'phys_address': '5e03.8002.0000',
                     'port_channel': {'port_channel_member': False},
                     'port_speed': '1000',
                     'port_speed_unit': 'Mb/s',
                     'reliability': '254/255',
                     'rxload': '1/255',
                     'txload': '1/255',
                     'types': 'Ethernet'}}}
        self.assertEqual(result, expected_output)
