import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting_appid_trunk_port


class TestConfigureAppHostingAppidTrunkPort(unittest.TestCase):

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
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_app_hosting_appid_trunk_port(self):
        result = configure_app_hosting_appid_trunk_port(self.device, '1key', 'AppGigabitEthernet', 2, 'trunk', None, 14, '172.15.0.1', '255.255.255.0', '172.15.0.255', True)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_app_hosting_appid_trunk_port_1(self):
        result = configure_app_hosting_appid_trunk_port(self.device, '1key1', 'management', None, None, 0, None, None, None, '172.15.0.255', False)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_app_hosting_appid_trunk_port_2(self):
        result = configure_app_hosting_appid_trunk_port(self.device, '1key2', 'AppGigabitEthernet', 2, 'trunk', None, 14, '172.15.0.1', '255.255.255.0', None, True)
        expected_output = None
        self.assertEqual(result, expected_output)
