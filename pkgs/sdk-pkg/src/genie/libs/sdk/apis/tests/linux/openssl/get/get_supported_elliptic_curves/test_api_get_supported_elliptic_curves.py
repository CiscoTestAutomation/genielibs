import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.openssl.get import get_supported_elliptic_curves


class TestGetSupportedEllipticCurves(unittest.TestCase):

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

    def test_get_supported_elliptic_curves(self):
        result = get_supported_elliptic_curves(self.device)
        expected_output = ['secp224r1', 'secp256k1', 'secp384r1', 'secp521r1', 'prime256v1']
        self.assertEqual(result, expected_output)
