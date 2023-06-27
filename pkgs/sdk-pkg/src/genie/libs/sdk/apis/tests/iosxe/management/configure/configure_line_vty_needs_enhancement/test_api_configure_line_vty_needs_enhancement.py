import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.management.configure import configure_line_vty_needs_enhancement


class TestConfigureLineVtyNeedsEnhancement(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T1-9400-Act:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9400
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['T1-9400-Act']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_line_vty_needs_enhancement(self):
        result = configure_line_vty_needs_enhancement(self.device, 0, 4, 0, 0)
        expected_output = None
        self.assertEqual(result, expected_output)
