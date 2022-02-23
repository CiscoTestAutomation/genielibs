import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.configure import unconfig_ip_on_vlan


class TestUnconfigIpOnVlan(unittest.TestCase):

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
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfig_ip_on_vlan(self):
        result = unconfig_ip_on_vlan(self.device, 10, '192.168.0.4', '255.255.255.0', '3001::30', 64)
        expected_output = None
        self.assertEqual(result, expected_output)
