from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_ipv6_acl


class TestUnconfigureIpv6Acl(TestCase):

    def test_unconfigure_ipv6_acl(self):
        self.device = Mock()
        unconfigure_ipv6_acl(self.device, 'A-scale6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ipv6 access-list A-scale6' ,)
        )
