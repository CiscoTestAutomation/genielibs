import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting_appid_docker


class TestConfigureAppHostingAppidDocker(unittest.TestCase):

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

    def test_configure_app_hosting_appid_docker(self):
        result = configure_app_hosting_appid_docker(self.device, '1key', True, [{'index': 3,
  'string': '-e TEAGENT_ACCOUNT_TOKEN=r3d29srpebr4j845lvnamwhswlori2xs'},
 {'index': 5, 'string': '-e TEAGENT_PROXY_TYPE=STATIC'},
 {'index': 7, 'string': '-e TEAGENT_PROXY_BYPASS_LIST=*.cisco.com'}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_app_hosting_appid_docker_1(self):
        result = configure_app_hosting_appid_docker(self.device, '1key1', False, [{'index': 3,
  'string': '-e TEAGENT_ACCOUNT_TOKEN=r3d29srpebr4j845lvnamwhswlori2xs'},
 {'index': 5, 'string': '-e TEAGENT_PROXY_TYPE=STATIC'},
 {'index': 7, 'string': '-e TEAGENT_PROXY_BYPASS_LIST=*.cisco.com'}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_app_hosting_appid_docker_2(self):
        result = configure_app_hosting_appid_docker(self.device, '1key2', True, [])
        expected_output = None
        self.assertEqual(result, expected_output)
