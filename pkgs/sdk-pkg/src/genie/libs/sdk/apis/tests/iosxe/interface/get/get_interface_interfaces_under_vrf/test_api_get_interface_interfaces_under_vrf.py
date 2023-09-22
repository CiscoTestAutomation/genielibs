import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_interfaces_under_vrf


class TestGetInterfaceInterfacesUnderVrf(unittest.TestCase):

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

    def test_get_interface_interfaces_under_vrf(self):
        result = get_interface_interfaces_under_vrf(self.device, 'VRF1')
        expected_output = [
            'GigabitEthernet2.390',
            'GigabitEthernet2.410',
            'GigabitEthernet2.415',
            'GigabitEthernet2.420',
            'GigabitEthernet3.390',
            'GigabitEthernet3.410',
            'GigabitEthernet3.415',
            'GigabitEthernet3.420',
            'Loopback300',
            'Tunnel1',
            'Tunnel3',
            'Tunnel4',
            'Tunnel6',
            'Tunnel8'
        ]
        self.assertEqual(result, expected_output)
