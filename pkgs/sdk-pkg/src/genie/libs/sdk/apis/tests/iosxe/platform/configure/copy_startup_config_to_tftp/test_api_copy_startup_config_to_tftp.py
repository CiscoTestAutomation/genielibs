import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import copy_startup_config_to_tftp


class TestCopyStartupConfigToTftp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_copy_startup_config_to_tftp(self):
        result = copy_startup_config_to_tftp(self.device, '202.153.144.25', '/auto/tftp-sjc-users4/nikhijai/startup_config_new', 30)
        expected_output = None
        self.assertEqual(result, expected_output)
