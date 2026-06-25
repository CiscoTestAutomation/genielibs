from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.interface.execute import execute_ping


class TestExecutePing(TestCase):

    def test_execute_ping(self):
        self.device = Mock()
        self.device.execute.return_value = (
            "Success rate is 91 percent (91/100), round-trip min/avg/max = 1/1/4 ms"
        )
        result = execute_ping(self.device, 'ip', '10.0.0.1')
        self.device.execute.assert_called_once_with(
            "ping ip 10.0.0.1 repeat 100 timeout 2"
        )
        self.assertEqual(result, 91)

    def test_execute_ping_custom_params(self):
        self.device = Mock()
        self.device.execute.return_value = (
            "Success rate is 100 percent (50/50), round-trip min/avg/max = 1/1/4 ms"
        )
        result = execute_ping(self.device, 'ipv6', '2001:db8::1', repeat=50, timeout=5)
        self.device.execute.assert_called_once_with(
            "ping ipv6 2001:db8::1 repeat 50 timeout 5"
        )
        self.assertEqual(result, 100)

    def test_execute_ping_no_match(self):
        self.device = Mock()
        self.device.execute.return_value = ""
        result = execute_ping(self.device, 'ip', '10.0.0.1')
        self.assertEqual(result, 0)

    def test_execute_ping_failure(self):
        self.device = Mock()
        self.device.execute.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            execute_ping(self.device, 'ip', '10.0.0.1')
