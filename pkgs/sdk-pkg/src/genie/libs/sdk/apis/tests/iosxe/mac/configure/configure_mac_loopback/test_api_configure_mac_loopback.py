import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mac.configure import configure_mac_loopback


class TestConfigureMacLoopback(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Speedracer:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat8k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Speedracer']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_mac_loopback(self):
        result = configure_mac_loopback(self.device, 'TenGigabitEthernet0/1/1')
        expected_output = None
        self.assertEqual(result, expected_output)
