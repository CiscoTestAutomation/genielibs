import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.eaptls.configure import unconfigure_crypto_key


class TestUnconfigureCryptoKey(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SecG-A2-8M9300:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SecG-A2-8M9300']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_crypto_key(self):
        result = unconfigure_crypto_key(self.device, 'SecG-A2-8M9300.cisco.com')
        expected_output = None
        self.assertEqual(result, expected_output)
