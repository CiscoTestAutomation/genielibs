import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.key.configure import generate_crypto_key_execute


class TestGenerateCryptoKeyExecute(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Startrek:
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
        self.device = self.testbed.devices['Startrek']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_generate_crypto_key_execute(self):
        result = generate_crypto_key_execute(self.device, 'rsa', '515')
        expected_output = None
        self.assertEqual(result, expected_output)