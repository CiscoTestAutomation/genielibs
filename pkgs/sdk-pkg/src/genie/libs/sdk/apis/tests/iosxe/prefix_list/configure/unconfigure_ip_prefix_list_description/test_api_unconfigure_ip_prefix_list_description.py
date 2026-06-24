import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.prefix_list.configure import (
    unconfigure_ip_prefix_list_description
)


class TestUnconfigureIpPrefixListDescription(unittest.TestCase):

    def test_unconfigure_ip_prefix_list_description(self):
        device = Mock()

        result = unconfigure_ip_prefix_list_description(
            device,
            'bgp_prefix',
            'this is bgp_prefix description'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip prefix-list bgp_prefix description this is bgp_prefix description',)
        )