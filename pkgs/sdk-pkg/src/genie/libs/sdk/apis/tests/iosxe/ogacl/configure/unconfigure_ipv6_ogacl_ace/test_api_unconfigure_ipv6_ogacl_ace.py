from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import unconfigure_ipv6_ogacl_ace


class TestUnconfigureIpv6OgaclAce(TestCase):

    def test_unconfigure_ipv6_ogacl_ace(self):
        device = Mock()
        result = unconfigure_ipv6_ogacl_ace(
            device=device,
            acl_name='ipv6-all-2',
            service_og='v6-serv-all',
            src_nw='v6-srcnet-all',
            dst_nw='any',
            rule='permit',
            service_type='',
            log_option='log',
            sequence_num=100
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ipv6 access-list ipv6-all-2\nno sequence 100 ',)
        )