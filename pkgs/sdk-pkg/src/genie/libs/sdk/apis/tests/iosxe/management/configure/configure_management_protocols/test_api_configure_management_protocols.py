import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_protocols


class TestConfigureManagementProtocols(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ott-c9300-67:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: cat9k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ott-c9300-67']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_management_protocols(self):
        result = configure_management_protocols(self.device, ['ssh', 'telnet', 'netconf', 'gnmi'])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_management_protocols_1(self):
        result = configure_management_protocols(self.device, ['ssh', 'telnet', 'netconf', {'gnmi': {'enable': True, 'server': True}}])
        expected_output = None
        self.assertEqual(result, expected_output)
