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
        result = configure_interface_monitor_session(self.device, [{'erspan_id': 301,
  'ip_address': '30.1.1.2',
  'mtu': 344,
  'origin_ip_address': '30.1.1.1',
  'session_name': 3,
  'session_type': 'erspan-source',
  'vlan_id': '100 rx',
  'vrf': 'red'}])
        expected_output = None
        self.assertEqual(result, expected_output)
