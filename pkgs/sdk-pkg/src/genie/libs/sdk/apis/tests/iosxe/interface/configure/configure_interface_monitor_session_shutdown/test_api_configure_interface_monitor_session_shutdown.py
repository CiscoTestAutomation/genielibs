import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_monitor_session_shutdown


class TestConfigureInterfaceMonitorSessionShutdown(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_monitor_session_shutdown(self):
        result = configure_interface_monitor_session_shutdown(self.device, [{'erspan_id': 1,
  'interface': 'TwentyFiveGigE2/1/1',
  'ip_address': '4.4.4.2',
  'origin_ip_address': '5.5.5.5',
  'session_name': 1,
  'session_type': 'erspan-source'}])
        expected_output = None
        self.assertEqual(result, expected_output)
