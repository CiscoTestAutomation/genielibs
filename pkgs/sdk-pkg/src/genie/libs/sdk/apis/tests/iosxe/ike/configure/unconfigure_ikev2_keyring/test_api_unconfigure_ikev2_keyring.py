import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ike.configure import unconfigure_ikev2_keyring


class TestUnconfigureIkev2Keyring(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Hub:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat8k
            model: c8000v
            pid: C8000V
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Hub']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ikev2_keyring(self):
        result = unconfigure_ikev2_keyring(self.device, 'HUB-KEY')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_ikev2_keyring_1(self):
        result = unconfigure_ikev2_keyring(self.device, 'HUB-KEY')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_ikev2_keyring_2(self):
        result = unconfigure_ikev2_keyring(self.device, 'dynamic')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_ikev2_keyring_3(self):
        result = unconfigure_ikev2_keyring(self.device, 'dynamic')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_ikev2_keyring_4(self):
        result = unconfigure_ikev2_keyring(self.device, 'manual')
        expected_output = None
        self.assertEqual(result, expected_output)
