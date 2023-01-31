import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_monitor_session


class TestConfigureInterfaceMonitorSession(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Intrepid_HA_DUT2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Intrepid_HA_DUT2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_monitor_session(self):
        result = configure_interface_monitor_session(self.device, [{'erspan_id': 1001,
  'interface': 'Fif2/0/1 rx',
  'ipv6_address': '2004::2',
  'origin_ipv6_address': '2040::1',
  'session_name': 2,
  'session_type': 'erspan-source'}])
        expected_output = None
        self.assertEqual(result, expected_output)
