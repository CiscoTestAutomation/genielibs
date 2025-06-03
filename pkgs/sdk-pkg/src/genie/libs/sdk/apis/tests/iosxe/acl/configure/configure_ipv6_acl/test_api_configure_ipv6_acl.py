from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_ipv6_acl


class TestConfigureIpv6Acl(TestCase):

    def test_configure_ipv6_acl(self):
        self.device = Mock()
        configure_ipv6_acl(self.device, 'acl_name', 'ipv6', 'any', 'any', 'deny', '', '', '', '', '10', 'time1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ipv6 access-list acl_name\nsequence 10 deny ipv6 any any time-range time1' ,)
        )
