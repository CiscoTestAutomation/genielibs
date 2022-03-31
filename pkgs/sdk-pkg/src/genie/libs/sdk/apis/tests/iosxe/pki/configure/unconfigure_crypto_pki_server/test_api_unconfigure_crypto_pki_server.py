import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.pki.configure import unconfigure_crypto_pki_server


class TestUnconfigureCryptoPkiServer(unittest.TestCase):

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

    def test_unconfigure_crypto_pki_server(self):
        result = unconfigure_crypto_pki_server(self.device, 'root')
        expected_output = True
        self.assertEqual(result, expected_output)
