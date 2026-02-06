from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.clear_ip_bgp_ipv6_unicast.util import clear_ip_bgp_ipv6_unicast


class TestClearIpBgpIpv6Unicast(TestCase):

    def test_clear_ip_bgp_ipv6_unicast(self):
        device = Mock()
        result = clear_ip_bgp_ipv6_unicast(device, 'unicast', 200)
        expected_output = None
        self.assertEqual(result, expected_output)

        # Verify execute was called with the correct command
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('clear ip bgp ipv6 unicast 200',)
        )


if __name__ == '__main__':
    import unittest
    unittest.main()