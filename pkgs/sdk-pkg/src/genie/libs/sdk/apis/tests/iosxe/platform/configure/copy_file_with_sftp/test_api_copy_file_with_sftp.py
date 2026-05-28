import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import copy_file_with_sftp
from genie.libs.sdk.apis.utils import sanitize


class TestCopyFileWithSftp(unittest.TestCase):

    def test_copy_file_with_sftp(self):
        device = Mock()

        device.execute.return_value = (
            'Destination filename [sh_ver.txt]? \r\n'
            '%Warning:There is a file already existing with this name \r\n'
            'Do you want to over write? [confirm]\r\n'
            'Sending file modes: C0644 3698 sh_ver.txt!\r\n'
            '3698 bytes copied in 0.304 secs (12164 bytes/sec)'
        )

        result = copy_file_with_sftp(
            device,
            '172.163.128.3',
            'sh_ver.txt',
            'root',
            'cisco',
            '.',
            1800
        )

        expected_output = (
            'Destination filename [sh_ver.txt]? \r\n'
            '%Warning:There is a file already existing with this name \r\n'
            'Do you want to over write? [confirm]\r\n'
            'Sending file modes: C0644 3698 sh_ver.txt!\r\n'
            '3698 bytes copied in 0.304 secs (12164 bytes/sec)'
        )

        self.assertEqual(sanitize(result), sanitize(expected_output))