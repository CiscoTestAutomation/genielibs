import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.get import get_device_uptime


class TestGetDeviceUptime(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          1783-CMS20DN:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: s5k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['1783-CMS20DN']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_device_uptime(self):
        result = get_device_uptime(self.device)
        expected_output = '5 weeks, 1 day, 23 hours, 24 minutes'
        self.assertEqual(result, expected_output)
