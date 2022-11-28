import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import get_show_output_exclude


class TestGetShowOutputExclude(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_show_output_exclude(self):
        result = get_show_output_exclude(self.device, 'show process memory', 0, None)
        expected_output = [True,
 ' lsmpi_io Pool Total:    6295128 Used:    6294296 Free:        832\r\n'
 '\r\n'
 ' PID TTY  Allocated      Freed    Holding    Getbufs    Retbufs Process\r\n'
 '                                326858784 Total']
        self.assertEqual(result, expected_output)
