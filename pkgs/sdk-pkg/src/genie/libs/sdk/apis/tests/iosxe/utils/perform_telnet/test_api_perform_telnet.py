import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import perform_telnet


class TestPerformTelnet(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SecG-A3-9410HA:
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
        self.device = self.testbed.devices['SecG-A3-9410HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_perform_telnet(self):
        result = perform_telnet(self.device, 'SecG-A3-9410HA', '10.8.12.26', 'admin1', 'cisco123', 'Mgmt-vrf', 'cisco123', 60)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_perform_telnet_1(self):
        result = perform_telnet(self.device, 'SecG-A3-9410HA', '100.8.12.5', 'admin1', 'cisco123', None, 'cisco123', 60)
        expected_output = True
        self.assertEqual(result, expected_output)
