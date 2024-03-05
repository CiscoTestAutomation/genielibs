import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.openssl.generate import generate_pkcs12


class TestGeneratePkcs12(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          sjc-ads-583:
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
        self.device = self.testbed.devices['sjc-ads-583']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_generate_pkcs12(self):
        result = generate_pkcs12(self.device, '/temp/secure/test_cert/device.key', '/temp/secure/test_cert/device.crt', '/temp/secure/test_cert/rootCA.crt', '/temp/secure/test_cert/device.p12', 'password', 'password')
        expected_output = None
        self.assertEqual(result, expected_output)
