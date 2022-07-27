import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_interfaces_status


class TestGetInterfacesStatus(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R1_xe:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: CSR1000v
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1_xe']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_interfaces_status(self):
        result = get_interfaces_status(self.device)
        expected_output = {'GigabitEthernet1': 'up',
 'GigabitEthernet2': 'up',
 'GigabitEthernet2.110': 'up',
 'GigabitEthernet2.115': 'up',
 'GigabitEthernet2.120': 'up',
 'GigabitEthernet2.390': 'up',
 'GigabitEthernet2.410': 'up',
 'GigabitEthernet2.415': 'up',
 'GigabitEthernet2.420': 'up',
 'GigabitEthernet2.90': 'up',
 'GigabitEthernet3': 'up',
 'GigabitEthernet3.110': 'up',
 'GigabitEthernet3.115': 'up',
 'GigabitEthernet3.120': 'up',
 'GigabitEthernet3.390': 'up',
 'GigabitEthernet3.410': 'up',
 'GigabitEthernet3.415': 'up',
 'GigabitEthernet3.420': 'up',
 'GigabitEthernet3.90': 'up',
 'GigabitEthernet4': 'up',
 'GigabitEthernet5': 'up',
 'GigabitEthernet6': 'up',
 'GigabitEthernet7': 'up',
 'Loopback0': 'up',
 'Loopback300': 'up',
 'Port-channel12': 'down',
 'Port-channel13': 'up',
 'Tunnel0': 'up',
 'Tunnel1': 'up',
 'Tunnel2': 'up',
 'Tunnel3': 'up',
 'Tunnel4': 'up',
 'Tunnel5': 'up',
 'Tunnel6': 'up',
 'Tunnel7': 'up',
 'Tunnel8': 'up',
 'Tunnel9': 'up'}
        self.assertEqual(result, expected_output)
