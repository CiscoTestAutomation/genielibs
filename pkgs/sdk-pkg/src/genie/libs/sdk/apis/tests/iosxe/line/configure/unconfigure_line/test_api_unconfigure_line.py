from unittest import TestCase
from genie.libs.sdk.apis.iosxe.line.configure import unconfigure_line
from unittest.mock import Mock


class TestUnconfigureLine(TestCase):

    def test_unconfigure_line(self):
        self.device = Mock()
        result = unconfigure_line(self.device, '0/3/0', 9600, 'even', 1, 8)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['line 0/3/0', 'no speed 9600', 'no parity even', 'no stopbits 1', 'no databits 8'],)
        )
