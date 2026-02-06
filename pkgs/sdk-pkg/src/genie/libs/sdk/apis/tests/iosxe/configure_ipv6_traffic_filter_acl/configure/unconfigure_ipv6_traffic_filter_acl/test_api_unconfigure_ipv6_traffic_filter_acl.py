from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.configure_ipv6_traffic_filter_acl.configure import unconfigure_ipv6_traffic_filter_acl


class TestUnconfigureIpv6TrafficFilterAcl(TestCase):

    def test_unconfigure_ipv6_traffic_filter_acl(self):
        device = Mock()
        result = unconfigure_ipv6_traffic_filter_acl(device, 11, 20, 'ipv6_md_acl', 'in')
        expected_output = None
        self.assertEqual(result, expected_output)

        # Verify configure was called with the correct commands
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface range vlan 11-20', 'no ipv6 traffic-filter ipv6_md_acl in'],)
        )


if __name__ == '__main__':
    import unittest
    unittest.main()