import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_mac_address


class TestGetInterfaceMacAddress(unittest.TestCase):

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
        self.device.connect()

    def test_get_interface_mac_address(self):
        result = get_interface_mac_address(self.device, 'GigabitEthernet1')
        expected_output = '5e01.4000.0000'
        self.assertEqual(result, expected_output)
