import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.key.configure import generate_crypto_key


class TestGenerateCryptoKey(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          INT1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['INT1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_generate_crypto_key(self):
        result = generate_crypto_key(self.device, 'ec', 'ECKEYS', None, '521', True, 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_generate_crypto_key_1(self):
        result = generate_crypto_key(self.device, 'ec', 'ECKEYS', None, '256', False, 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_generate_crypto_key_2(self):
        result = generate_crypto_key(self.device, 'ec', None, None, '384', True, 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_generate_crypto_key_3(self):
        result = generate_crypto_key(self.device, 'ec', None, None, '521', False, 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_generate_crypto_key_4(self):
        result = generate_crypto_key(self.device, 'rsa', 'RSAKEYS', '4096', None, True, 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_generate_crypto_key_5(self):
        result = generate_crypto_key(self.device, 'rsa', None, '4096', None, True, 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_generate_crypto_key_6(self):
        result = generate_crypto_key(self.device, 'rsa', None, None, None, True, 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_generate_crypto_key_7(self):
        result = generate_crypto_key(self.device, 'rsa', 'RSAKEYS', None, None, True, 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_generate_crypto_key_8(self):
        result = generate_crypto_key(self.device, 'rsa', None, '4096', None, False, 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_generate_crypto_key_9(self):
        result = generate_crypto_key(self.device, 'rsa', None, None, None, False, 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_generate_crypto_key_10(self):
        result = generate_crypto_key(self.device, 'rsa', 'RSAKEYS', None, None, False, 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_generate_crypto_key_11(self):
        result = generate_crypto_key(self.device, 'rsa', 'RSAKEYS', '4096', None, False, 30)
        expected_output = None
        self.assertEqual(result, expected_output)
