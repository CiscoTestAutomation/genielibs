import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ike.verify import verify_crypto_session_svti


class TestVerifyCryptoSessionSvti(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Hub:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: C8000V
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Hub']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_crypto_session_svti(self):
        result = verify_crypto_session_svti(self.device, 'Tunnel1', 'UP-ACTIVE', '5')
        expected_output = True
        self.assertEqual(result, expected_output)
