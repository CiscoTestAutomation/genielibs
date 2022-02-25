import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_profile_advanced


class TestConfigureIkev2ProfileAdvanced(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          TLS_Mad2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['TLS_Mad2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ikev2_profile_advanced(self):
        result = configure_ikev2_profile_advanced(self.device, 'IKEv2_PRFOILE', 'anyconnect-eap', 'rsa-sig', None, None, '10', '5', 'periodic', 'anyconnect-eap', 'aaa1', True, 'group', True, 'acvpn', 'gtc', 'user1', None, 'password1', True, True, 100, True, True, False, True, '1.1.1.1', False, None, None, None, True, 10, 3600, '2.2.2.2', None, None, False, None, False, None, None, None, None, None, True, 100, 'ID1', True, False, 'test', None, 600, False, False, 100, False, False)
        expected_output = None
        self.assertEqual(result, expected_output)
