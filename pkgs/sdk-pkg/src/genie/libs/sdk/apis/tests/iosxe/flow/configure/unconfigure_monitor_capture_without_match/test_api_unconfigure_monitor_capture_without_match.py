import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.flow.configure import unconfigure_monitor_capture_without_match


class TestUnconfigureMonitorCaptureWithoutMatch(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          starfleet-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['starfleet-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_monitor_capture_without_match(self):
        result = unconfigure_monitor_capture_without_match(self.device, 'REL', 'both', 'TwentyFiveGigE1/0/5')
        expected_output = None
        self.assertEqual(result, expected_output)
