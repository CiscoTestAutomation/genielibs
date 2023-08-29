import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.udld.configure import configure_udld_recovery


class TestConfigureUdldRecovery(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T2-9500-RA_SDG#:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['T2-9500-RA_SDG#']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_udld_recovery(self):
        result = configure_udld_recovery(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
