import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_authentication_event_server


class TestConfigureAuthenticationEventServer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9200L
            type: c9200L
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_authentication_event_server(self):
        result = configure_authentication_event_server(self.device, 'GigabitEthernet1/0/2', 'dead', 'authorize', '50')
        expected_output = None
        self.assertEqual(result, expected_output)
