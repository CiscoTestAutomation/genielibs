import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import configure_clear_logging_onboard_slot_voltage


class TestConfigureClearLoggingOnboardSlotVoltage(unittest.TestCase):

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
            platform: cat9400
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9404R-dut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_clear_logging_onboard_slot_voltage(self):
        result = configure_clear_logging_onboard_slot_voltage(self.device, 2)
        expected_output = None
        self.assertEqual(result, expected_output)
