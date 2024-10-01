import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.configure import configure_hostname


class TestConfigureHostname(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          test-device:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: cat9k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['test-device']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_hostname(self):
        result = configure_hostname(self.device, 'test-device')
        expected_output = None
        self.assertEqual(result, expected_output)
