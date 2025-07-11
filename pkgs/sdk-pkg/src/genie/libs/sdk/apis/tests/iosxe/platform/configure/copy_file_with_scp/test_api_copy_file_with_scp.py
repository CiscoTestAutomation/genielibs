import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import copy_file_with_scp
from genie.libs.sdk.apis.utils import sanitize

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
        self.maxDiff = None
        result = copy_file_with_scp(self.device, '172.163.128.3', 'sh_ver.txt', 'root', 'cisco', '.', 1800)
        expected_output = ('Destination filename [sh_ver.txt]? \r\n'
 '%Warning:There is a file already existing with this name \r\n'
 'Do you want to over write? [confirm]\r\n'
 ' Sending file modes: C0644 3698 sh_ver.txt\r\n'
 '!\r\n'
 '3698 bytes copied in 0.304 secs (12164 bytes/sec)')
        self.assertEqual(sanitize(result), sanitize(expected_output))

    def test_copy_file_with_scp_with_destination_username(self):
        self.maxDiff = None
        result = copy_file_with_scp(self.device, '10.64.69.167', 'request.pem.ca', 'navin', 'navin')
        expected_output = ('Destination username [navin]? \r\n'
 'Destination filename [request.pem]? \r\n'
 'Writing request.pem  Sink: C0644 1309 request.pem \r\n'
 '! \r\n'
 '1309 bytes copied in 0.267 secs (4903 bytes/sec)')
        # Device output inconsistently includes device prompt
        self.assertEqual(sanitize(result), sanitize(expected_output))
