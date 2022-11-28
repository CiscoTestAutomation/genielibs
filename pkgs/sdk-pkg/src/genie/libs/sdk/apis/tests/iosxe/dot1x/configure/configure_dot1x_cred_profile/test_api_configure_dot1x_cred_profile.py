import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_dot1x_cred_profile


class TestConfigureDot1xCredProfile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          stack-12m:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack-12m']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_dot1x_cred_profile(self):
        result = configure_dot1x_cred_profile(self.device, 'data_client', 'data_user1', 'cisco123', 'UNENCRYPTED')
        expected_output = None
        self.assertEqual(result, expected_output)
