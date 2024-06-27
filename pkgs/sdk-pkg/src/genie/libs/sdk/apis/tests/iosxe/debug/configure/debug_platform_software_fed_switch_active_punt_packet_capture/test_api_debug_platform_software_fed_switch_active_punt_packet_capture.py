import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.debug.configure import debug_platform_software_fed_switch_active_punt_packet_capture


class TestDebugPlatformSoftwareFedSwitchActivePuntPacketCapture(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9400-ha:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9400-ha']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_debug_platform_software_fed_switch_active_punt_packet_capture(self):
        result = debug_platform_software_fed_switch_active_punt_packet_capture(self.device, True, 10000, True, 257, True, 'ip', True, True, True)
        expected_output = None
        self.assertEqual(result, expected_output)
