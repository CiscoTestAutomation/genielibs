import unittest
from unittest.mock import MagicMock, Mock, call

from genie.libs.sdk.apis.iosxr.utils import get_md5_hash_of_file


class testMd5API(unittest.TestCase):

    def test_get_md5_hash_of_file(self):
        device = MagicMock()
        bash = device.bash_console.return_value.__enter__.return_value
        bash.execute = Mock(return_value='69c394d85d37fc15d445ae83155495e2  /harddisk:/test_file.bin')

        output = get_md5_hash_of_file(device, 'harddisk:/test_file.bin')

        bash.execute.assert_has_calls([call('md5sum /harddisk:/test_file.bin', timeout=60)])
        self.assertEqual(output, '69c394d85d37fc15d445ae83155495e2')

    def test_get_md5_hash_of_file_absolute_path(self):
        device = MagicMock()
        bash = device.bash_console.return_value.__enter__.return_value
        bash.execute = Mock(return_value='69c394d85d37fc15d445ae83155495e2  /harddisk:/test_file.bin')

        output = get_md5_hash_of_file(device, '/harddisk:/test_file.bin', timeout=120)

        bash.execute.assert_has_calls([call('md5sum /harddisk:/test_file.bin', timeout=120)])
        self.assertEqual(output, '69c394d85d37fc15d445ae83155495e2')

    def test_get_md5_hash_of_file_exception(self):
        device = MagicMock()
        bash = device.bash_console.return_value.__enter__.return_value
        bash.execute = Mock(side_effect=Exception('md5 failed'))

        output = get_md5_hash_of_file(device, 'harddisk:/test_file.bin')

        bash.execute.assert_has_calls([call('md5sum /harddisk:/test_file.bin', timeout=60)])
        self.assertIsNone(output)
