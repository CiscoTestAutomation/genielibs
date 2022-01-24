import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.eaptls.configure import unconfigure_crypto_pki_server


class TestUnconfigureCryptoPkiServer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          TGN2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['TGN2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_crypto_pki_server(self):
        result = unconfigure_crypto_pki_server(device=self.device, server_name='cisco')
        expected_output = None
        self.assertEqual(result, expected_output)
