import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.prefix_list.configure import (
    unconfigure_ip_prefix_list_seq
)


class TestUnconfigureIpPrefixListSeq(unittest.TestCase):

    def test_unconfigure_ip_prefix_list_seq(self):
        device = Mock()

        result = unconfigure_ip_prefix_list_seq(
            device,
            'bgp_prefix',
            '7.7.7.0',
            24,
            1,
            'deny',
            'ge',
            32
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
             (['no ip prefix-list bgp_prefix seq 1 deny 7.7.7.0/24 ge 32'],)
        )