import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_keyring


class TestConfigureIkev2Keyring(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Hub:
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
        self.device = self.testbed.devices['Hub']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ikev2_keyring(self):
        result = configure_ikev2_keyring(self.device, 'preshare', '1', '0.0.0.0', '0.0.0.0', 'cisco123', False, None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ikev2_keyring_1(self):
        result = configure_ikev2_keyring(self.device, 'manual', '1', '0.0.0.0', '0.0.0.0', None, False, 'ppk1', 'cisco123', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ikev2_keyring_2(self):
        result = configure_ikev2_keyring(self.device, 'manualrequired', '1', '0.0.0.0', '0.0.0.0', None, True, 'ppk2', 'cisco123', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ikev2_keyring_3(self):
        result = configure_ikev2_keyring(self.device, 'dynamic', '1', '0.0.0.0', '0.0.0.0', None, False, None, None, 'dynamic1')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ikev2_keyring_4(self):
        result = configure_ikev2_keyring(self.device, 'dynamicrequired', '1', '0.0.0.0', '0.0.0.0', None, True, None, None, 'dynamic2')
        expected_output = None
        self.assertEqual(result, expected_output)