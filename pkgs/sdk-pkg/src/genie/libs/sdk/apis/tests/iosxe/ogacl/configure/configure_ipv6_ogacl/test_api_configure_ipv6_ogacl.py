from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_ipv6_ogacl

class TestConfigureIpv6Ogacl(TestCase):

    def test_configure_ipv6_ogacl(self):
        device = Mock()
        result = configure_ipv6_ogacl(
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
            ('ipv6 access-list ipv6-all-2\nsequence 100 permit object-group v6-serv-all object-group v6-srcnet-all any log',)
        )