import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.utils import delete_files

class TestDeleteFiles(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.parse = Mock(return_value=Mock(
            q=Mock(contains_key_value=Mock(return_value=Mock(
                get_values=Mock(return_value=['file1.core'])
            )))
        ))
        self.device.execute = Mock()

    def test_delete_files_relative_path(self):
        result = delete_files(self.device, ['bootflash:/core'], ['file1.core'])
        self.device.execute.assert_called_with('delete /force bootflash:/core/file1.core')
        self.assertEqual(result, ['bootflash:/core/file1.core'])

    def test_delete_files_absolute_path(self):
        result = delete_files(self.device, ['bootflash:/core'], ['bootflash:/core/file1.core'])
        self.device.execute.assert_called_with('delete /force bootflash:/core/file1.core')
        self.assertEqual(result, ['bootflash:/core/file1.core'])


