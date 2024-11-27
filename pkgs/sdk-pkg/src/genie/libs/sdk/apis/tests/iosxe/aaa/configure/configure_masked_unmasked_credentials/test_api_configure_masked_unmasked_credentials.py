import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_masked_unmasked_credentials


class TestConfigureMaskedUnmaskedCredentials(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9200-3:
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
        self.device = self.testbed.devices['9200-3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_masked_unmasked_credentials(self):
        result = configure_masked_unmasked_credentials(self.device, 'USER', 'test', 15, 'POLICY', None, False, True, 'VIEW')
        expected_output = None
        self.assertEqual(result, expected_output)
