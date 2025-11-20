import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import copy_file_with_scp


class TestCopyFileWithScp(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_copy_file_with_scp(self):
        copy_file_with_scp(
            self.device, '172.163.128.3', 'sh_ver.txt',
            'root', 'cisco', '.', 1800
        )
        self.assertEqual(
            self.device.execute.mock_calls[0].args,
            ('copy scp://root:cisco@172.163.128.3/sh_ver.txt .',)
        )

    def test_copy_file_with_scp_with_destination_username(self):
        copy_file_with_scp(
            self.device, '10.64.69.167', 'request.pem.ca',
            'navin', 'navin'
        )
        self.assertEqual(
            self.device.execute.mock_calls[0].args,
            ('copy request.pem.ca scp://navin:navin@10.64.69.167/request.pem.ca',)
        )
