from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import unconfigure_ipv6_acl


class TestUnconfigureIpv6Acl(TestCase):

    def test_unconfigure_ipv6_acl(self):
        device = Mock()
        result = unconfigure_ipv6_acl(device=device, acl_name='ipv6-all-2')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ipv6 access-list ipv6-all-2',)
        )