import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.asr1k.configure import configure_boot_manual


class TestConfigureBootManual(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ott-asr1k-43:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: asr1k
            type: asr1k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ott-asr1k-43']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_boot_manual(self):
        result = configure_boot_manual(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
