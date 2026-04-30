import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.utils import get_filesystems


class TestGetFilesystems(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_filesystems_returns_all_prefixes_and_aliases(self):
        self.device.parse = Mock(return_value={
            'file_systems': {
                1: {'prefixes': 'crashinfo:'},
                2: {'prefixes': 'flash: bootflash:'},
                3: {'prefixes': 'sdflash:'},
            }
        })

        result = get_filesystems(self.device)

        self.device.parse.assert_called_once_with('show file systems')
        self.assertEqual(result, ['crashinfo:', 'flash:', 'bootflash:', 'sdflash:'])