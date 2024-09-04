import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.debug.configure import debug_platform_software_fed_drop_capture_action


class TestDebugPlatformSoftwareFedDropCaptureAction(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Intrepid-DUT4:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: None
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Intrepid-DUT4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_debug_platform_software_fed_drop_capture_action(self):
        result = debug_platform_software_fed_drop_capture_action(self.device, 'clear-statistics', 'active', None)
        expected_output = None
        self.assertEqual(result, expected_output)
