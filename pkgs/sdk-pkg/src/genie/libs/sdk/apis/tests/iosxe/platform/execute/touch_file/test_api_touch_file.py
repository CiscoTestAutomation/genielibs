from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.platform.execute import touch_file


class TestTouchFile(TestCase):

    def test_touch_file(self):
        device = Mock()

        touch_file(device, directory='bootflash:/', file_name='test.txt')

        device.tclsh.assert_called_once_with('puts [open "bootflash:/test.txt" w+] {}')
