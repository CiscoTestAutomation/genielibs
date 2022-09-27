import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_access_session_port_control


class TestConfigureAccessSessionPortControl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          nyq4:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['nyq4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_access_session_port_control(self):
        result = configure_access_session_port_control(self.device, ' TenGigabitEthernet1/1/7', 'auto')
        expected_output = None
        self.assertEqual(result, expected_output)
