import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting_resource_profile


class TestConfigureAppHostingResourceProfile(unittest.TestCase):

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

    def test_configure_app_hosting_resource_profile(self):
        result = configure_app_hosting_resource_profile(self.device, '1key', 'custom', 40, 30, 4000, 5666, True)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_app_hosting_resource_profile_1(self):
        result = configure_app_hosting_resource_profile(self.device, '1key1', 'custom', 40, None, 4000, 5666, False)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_app_hosting_resource_profile_2(self):
        result = configure_app_hosting_resource_profile(self.device, '1key', 'custom', 40, None, None, 5666, False)
        expected_output = None
        self.assertEqual(result, expected_output)
