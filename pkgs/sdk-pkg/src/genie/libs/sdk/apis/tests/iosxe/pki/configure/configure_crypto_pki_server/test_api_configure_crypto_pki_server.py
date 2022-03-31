import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.pki.configure import configure_crypto_pki_server


class TestConfigureCryptoPkiServer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          vm5006:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['vm5006']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_crypto_pki_server(self):
        result = configure_crypto_pki_server(self.device, 'root', 'Cisco', '7 2 32', 'http', 'cisco.com', 'abc.crl', 'pem', 'Cisco123', 'minimum', 'http', 'ciscoo.com', 'cnm', True, 'email-protection ocsp-signing server-auth', 'auto', None, None, None, 'md5', 'CN=R1', '45 2', '45 3 3', None, None, None, False, '0x44', None, None, 'crl ocsp none', 2048, 80)
        expected_output = True
        self.assertEqual(result, expected_output)
