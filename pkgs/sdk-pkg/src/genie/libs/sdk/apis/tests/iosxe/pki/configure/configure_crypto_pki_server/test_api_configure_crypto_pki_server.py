import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.pki.configure import configure_crypto_pki_server


class TestConfigureCryptoPkiServer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          fugazi:
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
        self.device = self.testbed.devices['fugazi']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_crypto_pki_server(self):
        result = configure_crypto_pki_server(self.device, 'ca', 'cisco123', None, None, None, None, 'pkcs12', 'cisco123', None, 'bootflash:', None, 'p12', False, None, 'auto', None, None, None, None, None, None, None, None, None, None, False, None, None, None, None, None, 80)
        expected_output = True
        self.assertEqual(result, expected_output)
