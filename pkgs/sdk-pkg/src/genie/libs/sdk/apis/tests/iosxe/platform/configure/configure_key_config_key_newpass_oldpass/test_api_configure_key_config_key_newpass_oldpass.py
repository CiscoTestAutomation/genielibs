import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import configure_key_config_key_newpass_oldpass


class TestConfigureKeyConfigKeyNewpassOldpass(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          pki-reg2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c8000v
            type: c8000v
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['pki-reg2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_key_config_key_newpass_oldpass(self):
        result = configure_key_config_key_newpass_oldpass(self.device, 'test4567', 'cisco123')
        expected_output = None
        self.assertEqual(result, expected_output)
