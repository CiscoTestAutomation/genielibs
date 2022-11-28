import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_crypto_ikev2_policy


class TestConfigureCryptoIkev2Policy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Arcade1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Arcade1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_crypto_ikev2_policy(self):
        result = configure_crypto_ikev2_policy(self.device, 'newpolicy', 'newproposal', 'any')
        expected_output = None
        self.assertEqual(result, expected_output)
