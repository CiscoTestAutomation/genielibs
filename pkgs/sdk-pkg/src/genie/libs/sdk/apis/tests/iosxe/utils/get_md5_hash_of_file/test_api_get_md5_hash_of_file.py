import os
import unittest
from textwrap import dedent
from unittest.mock import Mock, call

from genie.libs.sdk.apis.iosxe.utils import get_md5_hash_of_file

class testAPI(unittest.TestCase):

    def test_get_md5_hash_of_file(self):
        mock = Mock()
        mock.execute = Mock(return_value=dedent('''
        .......................Done!

        verify /md5 (bootflash:filename) = 688e630cfeb8a80fa553fb5464650e1d

        '''))
        output = get_md5_hash_of_file(mock, 'filename')

        mock.execute.assert_has_calls([call('verify /md5 filename', timeout=180)])
        self.assertEqual(output, '688e630cfeb8a80fa553fb5464650e1d')

