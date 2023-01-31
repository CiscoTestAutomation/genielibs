import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.flow.configure import configure_monitor_capture_match


class TestConfigureMonitorCaptureMatch(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          tmbs1:
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
        self.device = self.testbed.devices['tmbs1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_monitor_capture_match(self):
        result = configure_monitor_capture_match(self.device, 'REL', 'ipv4', 'host', '3.3.3.3', '4.5.5.4')
        expected_output = None
        self.assertEqual(result, expected_output)
