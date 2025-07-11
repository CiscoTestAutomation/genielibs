from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_ipv6_acl_ace


class TestUnconfigureIpv6AclAce(TestCase):

    def test_unconfigure_ipv6_acl_ace(self):
        self.device = Mock()
        unconfigure_ipv6_acl_ace(device=self.device, acl_name='racl-1', service_type='tcp', src_nw='2013:1::20', dst_nw='2013:1::10', rule='permit', host_option=True, prefix='', dst_port='179', log_option='log', sequence_num='200')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ipv6 access-list racl-1\nno sequence 200 ' ,)
        )
