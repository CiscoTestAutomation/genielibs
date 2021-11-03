import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.configure import config_ip_on_vlan


class TestConfigIpOnVlan(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          sisf-c9500-21-8-26-2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ios
            type: ios
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sisf-c9500-21-8-26-2']
        self.device.connect()

    def test_config_ip_on_vlan(self):
        result = config_ip_on_vlan(self.device, 251, '192.168.1.1', '255.255.255.0', '2001::3', 10)
        expected_output = None
        self.assertEqual(result, expected_output)
