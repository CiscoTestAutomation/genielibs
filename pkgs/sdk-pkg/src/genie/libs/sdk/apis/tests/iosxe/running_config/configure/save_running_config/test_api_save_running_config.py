import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.running_config.configure import save_running_config


class TestSaveRunningConfig(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          iolpe2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iol
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['iolpe2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_save_running_config(self):
        result = save_running_config(self.device, 'running-config', 'startup-config', '30')
        expected_output = None
        self.assertEqual(result, expected_output)
