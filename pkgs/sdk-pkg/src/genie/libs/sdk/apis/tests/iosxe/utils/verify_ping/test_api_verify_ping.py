
import unittest
from textwrap import dedent
from unittest.mock import MagicMock, Mock, call

from genie.libs.sdk.apis.iosxe.utils import verify_ping


class TestUtilsApi(unittest.TestCase):

    def test_verify_ping_vrf(self):
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

    def test_verify_ping_vrf_source(self):
        device = Mock()

        output = dedent("""
            ping vrf Mgmt-vrf 127.0.0.1 source Loopback0
            Type escape sequence to abort.
            Sending 5, 100-byte ICMP Echos to 127.0.0.1, timeout is 2 seconds:
            .....
            Success rate is 0 percent (0/5)
            """)

        device.execute = Mock(return_value = output)
        result = verify_ping(device, vrf='Mgmt-vrf', address='127.0.0.1', source='Loopback0',
                             check_interval=0.1, max_time=0.2)
        self.assertEqual(result, False)
        device.execute.assert_has_calls([
            call('ping vrf Mgmt-vrf 127.0.0.1 source Loopback0',
                 error_pattern=['% No valid source address for destination'])
        ])

    def test_verify_ping_count(self):
        device = Mock()

        output = dedent("""
            ping 127.0.0.1 repeat 2
            Type escape sequence to abort.
            Sending 5, 100-byte ICMP Echos to 127.0.0.1, timeout is 2 seconds:
            .....
            Success rate is 0 percent (0/5)
            """)

        device.execute = Mock(return_value = output)
        result = verify_ping(device, address='127.0.0.1', count=2, check_interval=0.1, max_time=0.2)
        self.assertEqual(result, False)
        device.execute.assert_has_calls([
            call('ping 127.0.0.1 repeat 2',
                 error_pattern=['% No valid source address for destination'])
        ])

    def test_verify_ping_count_source(self):
        device = Mock()

        output = dedent("""
            ping 127.0.0.1 source Loopback0 repeat 2
            Type escape sequence to abort.
            Sending 5, 100-byte ICMP Echos to 127.0.0.1, timeout is 2 seconds:
            .....
            Success rate is 0 percent (0/5)
            """)

        device.execute = Mock(return_value = output)
        result = verify_ping(device, address='127.0.0.1', count=2, source='Loopback0',
                             check_interval=0.1, max_time=0.2)
        self.assertEqual(result, False)
        device.execute.assert_has_calls([
            call('ping 127.0.0.1 source Loopback0 repeat 2',
                 error_pattern=['% No valid source address for destination'])
        ])

    def test_verify_ping_size(self):
        device = Mock()

        output = dedent("""
            ping 127.0.0.1 size 36
            Type escape sequence to abort.
            Sending 5, 100-byte ICMP Echos to 127.0.0.1, timeout is 2 seconds:
            .....
            Success rate is 0 percent (0/5)
            """)

        device.execute = Mock(return_value = output)
        result = verify_ping(device, address='127.0.0.1', size=36,
                             check_interval=0.1, max_time=0.2)
        self.assertEqual(result, False)
        device.execute.assert_has_calls([
            call('ping 127.0.0.1 size 36',
                 error_pattern=['% No valid source address for destination'])
        ])
