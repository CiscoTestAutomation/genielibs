import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.running_config.configure import configure_replace


class TestConfigureReplace(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9300-24UX-1:
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
        self.device = self.testbed.devices['9300-24UX-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_replace(self):
        result = configure_replace(self.device, 'flash:', 'new_config', '', 1, 60)
        expected_output = ('This will apply all necessary additions and deletions\r\n'
 'to replace the current running configuration with the\r\n'
 'contents of the specified configuration file, which is\r\n'
 'assumed to be a complete configuration, not a partial\r\n'
 'configuration. Enter Y if you are sure you want to proceed. ? [no]:Y')
        self.assertEqual(result, expected_output)
