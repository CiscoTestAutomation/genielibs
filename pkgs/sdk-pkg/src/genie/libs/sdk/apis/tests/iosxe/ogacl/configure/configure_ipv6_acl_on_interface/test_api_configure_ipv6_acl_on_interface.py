from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_ipv6_acl_on_interface

class TestConfigureIpv6AclOnInterface(TestCase):

    def test_configure_ipv6_acl_on_interface(self):
        device = Mock()
        result = configure_ipv6_acl_on_interface(
            device=device,
            interface='HundredGigE1/0/21',
            acl_name='ipv6-all-2',
            inbound=True
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('interface HundredGigE1/0/21\nipv6 traffic-filter ipv6-all-2 in',)
        )