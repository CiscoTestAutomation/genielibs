import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.verify import verify_pattern_in_show_logging
import re


class TestVerifyPatternInShowLogging(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          C9200-Standalone:
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
        self.device = self.testbed.devices['C9200-Standalone']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_pattern_in_show_logging(self):
        # Switch 1 R0/0: dmiauthd: Configuration change requiring running configuration
        p1 = re.compile(r".*%DMI-5-SYNC_NEEDED:\s*Switch\s*\d*\s*R\d*\/\d*:\s*dmiauthd:"
                        r"\s*Configuration\s*change\s*requiring\s*running\s*configuration"
                        r"\s*sync\s*detected")

        # sync detected - '  line console 0'. The running configuration will be synchronized
        p2 = re.compile(r".*%DMI-5-SYNC_START:\s*Switch\s*\d*\s*R\d*\/\d*:\s*dmiauthd:"
                        r"\s*Synchronization\s*of\s*the\s*running\s*configuration\s*to"
                        r"\s*the\s*NETCONF\s*running\s*data\s*store\s*has\s*started")

        pattern_list = [p1, p2]
        result = verify_pattern_in_show_logging(self.device, pattern_list)
        expected_output = True
        self.assertEqual(result, expected_output)
