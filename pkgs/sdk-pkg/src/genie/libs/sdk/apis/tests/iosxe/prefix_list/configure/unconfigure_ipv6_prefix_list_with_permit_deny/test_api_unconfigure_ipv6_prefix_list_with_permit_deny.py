from unittest import TestCase
from genie.libs.sdk.apis.iosxe.prefix_list.configure import unconfigure_ipv6_prefix_list_with_permit_deny
from unittest.mock import Mock


class TestUnconfigureIpv6PrefixListWithPermitDeny(TestCase):

    def test_unconfigure_ipv6_prefix_list_with_permit_deny(self):
        self.device = Mock()
        result = unconfigure_ipv6_prefix_list_with_permit_deny(self.device, 'list_name', 'permit', '1:1::', '24', 20, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ipv6 prefix-list list_name seq 20 permit 1:1::/24'],)
        )
