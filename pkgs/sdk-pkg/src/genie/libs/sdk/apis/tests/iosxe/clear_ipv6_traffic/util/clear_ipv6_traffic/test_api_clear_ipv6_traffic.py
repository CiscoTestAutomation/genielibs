from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.clear_ipv6_traffic.util import clear_ipv6_traffic


class TestClearIpv6Traffic(TestCase):

    def test_clear_ipv6_traffic(self):
        device = Mock()
        result = clear_ipv6_traffic(device)
        expected_output = None
        self.assertEqual(result, expected_output)

        # Verify execute was called with the correct command
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('clear ipv6 traffic',)
        )


if __name__ == '__main__':
    import unittest
    unittest.main()