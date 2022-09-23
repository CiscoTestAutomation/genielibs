import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.key.clear import crypto_key_zeroize


class TestCryptoKeyZeroize(unittest.TestCase):

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

    def test_crypto_key_zeroize(self):
        result = crypto_key_zeroize(self.device, 'rsa', 'RSAKEYS', 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_crypto_key_zeroize_1(self):
        result = crypto_key_zeroize(self.device, 'rsa ', '', 30)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_crypto_key_zeroize_2(self):
        result = crypto_key_zeroize(self.device, '', '', 30)
        expected_output = None
        self.assertEqual(result, expected_output)
