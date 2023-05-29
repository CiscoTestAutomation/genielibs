import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.execute import execute_app_hosting_appid


class TestExecuteAppHostingAppid(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyq-PE1:
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
        self.device = self.testbed.devices['stack3-nyq-PE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_app_hosting_appid(self):
        result = execute_app_hosting_appid(self.device, 12, 'activate', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_execute_app_hosting_appid_1(self):
        result = execute_app_hosting_appid(self.device, 9, 'install', 'flash:test.txt')
        expected_output = None
        self.assertEqual(result, expected_output)
