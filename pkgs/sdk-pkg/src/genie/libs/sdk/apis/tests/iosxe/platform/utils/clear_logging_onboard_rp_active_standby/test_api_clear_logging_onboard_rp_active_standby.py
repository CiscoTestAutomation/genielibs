import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.utils import clear_logging_onboard_rp_active_standby


class TestClearLoggingOnboardRpActiveStandby(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9404R-dut1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9404R-dut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_logging_onboard_rp_active_standby(self):
        result = clear_logging_onboard_rp_active_standby(self.device, 'active', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_logging_onboard_rp_active_standby_1(self):
        result = clear_logging_onboard_rp_active_standby(self.device, 'active', 'temperature')
        expected_output = None
        self.assertEqual(result, expected_output)
