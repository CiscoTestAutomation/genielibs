import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import platform_hardware_fed_switch_phy_debug


class TestPlatformHardwareFedSwitchPhyDebug(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          hendrix:
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
        self.device = self.testbed.devices['hendrix']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_platform_hardware_fed_switch_phy_debug(self):
        result = platform_hardware_fed_switch_phy_debug(self.device, 'active', 1, 'MCUDebugLogs')
        expected_output = None
        self.assertEqual(result, expected_output)
