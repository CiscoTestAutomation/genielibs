from unittest import TestCase
from genie.libs.sdk.apis.iosxe.prefix_list.configure import configure_ipv6_prefix_list_with_permit_deny
from unittest.mock import Mock


class TestConfigureIpv6PrefixListWithPermitDeny(TestCase):

    def test_configure_ipv6_prefix_list_with_permit_deny(self):
        self.device = Mock()
        result = configure_ipv6_prefix_list_with_permit_deny(self.device, 'list_name', 'permit', '1:1::', '24', 20, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 prefix-list list_name seq 20 permit 1:1::/24'],)
        )
