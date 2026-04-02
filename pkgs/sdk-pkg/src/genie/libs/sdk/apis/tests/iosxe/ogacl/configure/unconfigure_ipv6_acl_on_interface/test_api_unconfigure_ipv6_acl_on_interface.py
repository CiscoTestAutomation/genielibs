from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import unconfigure_ipv6_acl_on_interface


class TestUnconfigureIpv6AclOnInterface(TestCase):

    def test_unconfigure_ipv6_acl_on_interface(self):
        device = Mock()
        result = unconfigure_ipv6_acl_on_interface(
            device=device,
            interface='HundredGigE1/0/21',
            acl_name='racl-1',
            inbound=True
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('interface HundredGigE1/0/21\nno ipv6 traffic-filter racl-1 in',)
        )