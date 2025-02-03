from unittest import TestCase
from genie.libs.sdk.apis.iosxe.line.configure import configure_line
from unittest.mock import Mock


class TestConfigureLine(TestCase):

    def test_configure_line(self):
        self.device = Mock()
        result = configure_line(self.device, '0/3/0', 9600, 'even', 1, 8)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['line 0/3/0', 'speed 9600', 'parity even', 'stopbits 1', 'databits 8'],)
        )
