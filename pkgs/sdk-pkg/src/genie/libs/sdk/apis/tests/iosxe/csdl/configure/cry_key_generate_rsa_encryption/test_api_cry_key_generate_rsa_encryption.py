import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.csdl.configure import cry_key_generate_rsa_encryption


class TestCryKeyGenerateRsaEncryption(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          3850-48XS-CE3:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['3850-48XS-CE3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_cry_key_generate_rsa_encryption(self):
        result = cry_key_generate_rsa_encryption(self.device, '2048', 'BillRSAkey1')
        expected_output = None
        self.assertEqual(result, expected_output)
