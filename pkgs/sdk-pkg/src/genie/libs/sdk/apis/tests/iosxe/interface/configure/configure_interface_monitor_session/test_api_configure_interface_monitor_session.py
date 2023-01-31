import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_monitor_session


class TestConfigureInterfaceMonitorSession(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Cat9500H_SVL_DUT3:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Cat9500H_SVL_DUT3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_monitor_session(self):
        result = configure_interface_monitor_session(self.device, [{'erspan_id': 101,
  'interface': 'Twe1/0/7',
  'ipv6_address': '2040::1',
  'session_name': 6,
  'session_type': 'erspan-destination'}])
        expected_output = None
        self.assertEqual(result, expected_output)
