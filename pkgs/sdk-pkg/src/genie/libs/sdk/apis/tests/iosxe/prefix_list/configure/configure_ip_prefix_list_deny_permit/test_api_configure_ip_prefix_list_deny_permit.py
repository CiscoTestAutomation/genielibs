import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.prefix_list.configure import (
    configure_ip_prefix_list_deny_permit
)


class TestConfigureIpPrefixListDenyPermit(unittest.TestCase):

    def test_configure_ip_prefix_list_deny_permit(self):
        device = Mock()

        result = configure_ip_prefix_list_deny_permit(
            device,
            'bgp_prefix',
            'deny',
            '7.7.7.0',
            24,
            'ge',
            32
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip prefix-list bgp_prefix deny 7.7.7.0/24 ge 32'],)
        )