import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import clear_configuration_lock


class TestClearConfigurationLock(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          c8kv-2065:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c8kv
            type: c8kv
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['c8kv-2065']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_configuration_lock(self):
        result = clear_configuration_lock(self.device)
        expected_output = 'Configuration mode is not locked.'
        self.assertEqual(result, expected_output)
