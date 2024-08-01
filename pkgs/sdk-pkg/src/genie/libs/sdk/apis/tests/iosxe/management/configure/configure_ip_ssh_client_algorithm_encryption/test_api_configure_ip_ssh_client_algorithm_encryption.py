import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.management.configure import configure_ip_ssh_client_algorithm_encryption


class TestConfigureIpSshClientAlgorithmEncryption(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Bonjour_mDNS:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Bonjour_mDNS']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_ssh_client_algorithm_encryption(self):
        result = configure_ip_ssh_client_algorithm_encryption(self.device, 'aes256-gcm')
        expected_output = None
        self.assertEqual(result, expected_output)
