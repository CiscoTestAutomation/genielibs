import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.span.configure import configure_interface_monitor_session_no_mtu


class TestConfigureInterfaceMonitorSessionNoMtu(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Gryphon-9500-SVL:
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
        self.device = self.testbed.devices['Gryphon-9500-SVL']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_monitor_session_no_mtu(self):
        result = configure_interface_monitor_session_no_mtu(self.device, '2', '1500')
        expected_output = None
        self.assertEqual(result, expected_output)
