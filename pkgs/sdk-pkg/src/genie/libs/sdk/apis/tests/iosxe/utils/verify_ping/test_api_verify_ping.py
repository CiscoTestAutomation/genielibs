
import unittest
from textwrap import dedent
from unittest.mock import MagicMock, Mock, call

from genie.libs.sdk.apis.iosxe.utils import verify_ping


class TestUtilsApi(unittest.TestCase):

    def test_verify_ping(self):
        device = Mock()

        output = dedent("""
            ping vrf Mgmt-vrf 127.0.0.1
            Type escape sequence to abort.
            Sending 5, 100-byte ICMP Echos to 127.0.0.1, timeout is 2 seconds:
            .....
            Success rate is 0 percent (0/5)
            """)

        device.execute = Mock(return_value = output)
        result = verify_ping(device, vrf='Mgmt-vrf', address='127.0.0.1', check_interval=0.1, max_time=0.2)
        self.assertEqual(result, False)
        device.execute.assert_has_calls([
            call('ping vrf Mgmt-vrf 127.0.0.1', error_pattern=['% No valid source address for destination'])
        ])

