import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.verify import verify_last_reload_reason


class TestVerifyLastReloadReason(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          IE-3300-8P2S-E3:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ie3300
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['IE-3300-8P2S-E3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_last_reload_reason(self):
        result = verify_last_reload_reason(self.device, 'Power Cycle')
        expected_output = False
        self.assertEqual(result, expected_output)
