import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.openssl.generate import generate_ssl_certificate


class TestGenerateSslCertificate(unittest.TestCase):

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

    def test_generate_ssl_certificate(self):
        result = generate_ssl_certificate(self.device, '/users/lgerrior/test_dir/ecc_private_key', '/users/lgerrior/test_dir/rootCA.pem', '/users/lgerrior/test_dir/rsa_private_key', 'cisco123', 'cisco123', None, None, None, '/users/lgerrior/test_dir', 256)
        expected_output = None
        self.assertEqual(result, expected_output)
