import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.pki.configure import configure_crypto_pki_profile


class TestConfigureCryptoPkiProfile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          dut1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c8000v
            type: c8000v
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['dut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_crypto_pki_profile(self):
        result = configure_crypto_pki_profile(self.device, 'API_PROF', True, 'ashrishe', '0', 'nopassword', 'https://10.106.29.252:443', None, True, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)
