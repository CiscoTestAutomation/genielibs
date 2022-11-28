import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_aaa_methods


class TestConfigureCtsAaaMethods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          MOHMA_SCORPION:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['MOHMA_SCORPION']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_cts_aaa_methods(self):
        result = configure_cts_aaa_methods(self.device, 'test_ise', 'cts_test')
        expected_output = None
        self.assertEqual(result, expected_output)
