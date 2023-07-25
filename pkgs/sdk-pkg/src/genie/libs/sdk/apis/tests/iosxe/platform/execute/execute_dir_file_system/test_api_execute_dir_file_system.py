import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_dir_file_system


class TestExecuteDirFileSystem(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Sanity-ASR2X:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Sanity-ASR2X']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_dir_file_system(self):
        result = execute_dir_file_system(self.device, 'bootflash:', 'test', 120)
        expected_output = ('Directory of bootflash:/test/\r\n'
 '\r\n'
 'No files in directory\r\n'
 '\r\n'
 '6646632448 bytes total (3948212224 bytes free)')
        self.assertEqual(result, expected_output)
