import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mac.execute import monitor_event_trace_clear


class TestMonitorEventTraceClear(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Prasad_9500X:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Prasad_9500X']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_monitor_event_trace_clear(self):
        result = monitor_event_trace_clear(self.device, 'vlan', 'critical')
        expected_output = None
        self.assertEqual(result, expected_output)
