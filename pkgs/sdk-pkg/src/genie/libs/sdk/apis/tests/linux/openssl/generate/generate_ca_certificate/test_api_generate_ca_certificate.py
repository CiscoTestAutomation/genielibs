import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.openssl.generate import generate_ca_certificate


class TestGenerateCaCertificate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          S1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os linux --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: linux
            platform: None
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['S1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_generate_ca_certificate(self):
        result = generate_ca_certificate(self.device, '/users/lgerrior/test_dir/rsa_private_key', None, 'cisco123', None, '/users/lgerrior/test_dir')
        expected_output = None
        self.assertEqual(result, expected_output)
