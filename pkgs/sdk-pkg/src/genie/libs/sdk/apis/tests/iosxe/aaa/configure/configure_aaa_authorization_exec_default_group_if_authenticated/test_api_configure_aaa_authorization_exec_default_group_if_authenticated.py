import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authorization_exec_default_group_if_authenticated


class TestConfigureAaaAuthorizationExecDefaultGroupIfAuthenticated(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          security-gryphon2:
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
        self.device = self.testbed.devices['security-gryphon2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_aaa_authorization_exec_default_group_if_authenticated(self):
        result = configure_aaa_authorization_exec_default_group_if_authenticated(self.device, 'TACACS-group')
        expected_output = None
        self.assertEqual(result, expected_output)
