import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat8k.configure import configure_mode_change


class TestConfigureModeChange(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          encore_sanity:
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
        self.device = self.testbed.devices['encore_sanity']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_mode_change(self):
        result = configure_mode_change(self.device, '0/1', '40G', 60)
        expected_output = None
        self.assertEqual(result, expected_output)
