import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.c9500.C9500_24Y4C.configure import configure_ignore_startup_config


class TestConfigureIgnoreStartupConfig(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ott-c9500-66:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
            pid: C9500-24Y4C
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ott-c9500-66']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ignore_startup_config(self):
        result = configure_ignore_startup_config(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
