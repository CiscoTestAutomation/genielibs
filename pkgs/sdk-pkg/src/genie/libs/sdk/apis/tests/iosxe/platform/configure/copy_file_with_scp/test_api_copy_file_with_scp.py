import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import copy_file_with_scp


class TestCopyFileWithScp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          VCR:
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
        self.device = self.testbed.devices['VCR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_copy_file_with_scp(self):
        result = copy_file_with_scp(self.device, '172.163.128.3', 'sh_switch_sftp.txt', 'root', 'cisco', None, 30)
        expected_output = ('Address or name of remote host [172.163.128.3]? \r\n'
 'Destination filename [sh_switch_sftp.txt]? \r\n'
 'Writing sh_switch_sftp.txt  Sink: C0644 397 sh_switch_sftp.txt\r\n'
 '!\r\n'
 '397 bytes copied in 0.200 secs (1985 bytes/sec)')
        # Device output inconsistently includes device prompt
        if result.endswith('#'):
            expected_output += '\r\nT13-C9300-24T#'
        self.assertEqual(result, expected_output)
