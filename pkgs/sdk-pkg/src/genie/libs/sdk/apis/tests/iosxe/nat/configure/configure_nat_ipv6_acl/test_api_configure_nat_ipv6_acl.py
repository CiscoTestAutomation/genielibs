from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat_ipv6_acl

class TestConfigureNatIpv6Acl(TestCase):

    def test_configure_nat_ipv6_acl(self):
        device = Mock()
        result = configure_nat_ipv6_acl(device, 'acl_4', 'permit', '2001:1::/64', 10)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'ipv6 access-list acl_4',
                'permit ipv6 2001:1::/64 any sequence 10'
            ],)
        )