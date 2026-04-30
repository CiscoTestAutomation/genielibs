from unittest import TestCase
from unittest.mock import MagicMock, call

from genie.libs.sdk.apis.iosxe.ie3k.platform.execute import touch_file


class TestTouchFile(TestCase):

    def test_touch_file(self):
        device = MagicMock()
        bash = MagicMock()
        device.bash_console.return_value.__enter__.return_value = bash

        touch_file(device, directory='bootflash:/', file_name='test.txt')

        bash.execute.assert_called_once_with('touch bootflash/test.txt')
        device.execute.assert_has_calls([
            call('set platform software selinux permissive'),
            call('set platform software selinux default')
        ])
