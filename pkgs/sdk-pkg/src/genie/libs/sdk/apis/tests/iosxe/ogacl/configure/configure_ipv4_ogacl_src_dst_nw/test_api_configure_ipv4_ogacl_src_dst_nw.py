from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_ipv4_ogacl_src_dst_nw

class TestConfigureIpv4OgaclSrcDstNw(TestCase):

    def test_configure_ipv4_ogacl_src_dst_nw(self):
        device = Mock()
        result = configure_ipv4_ogacl_src_dst_nw(
            device, 'ogacl_policy_in', 'permit', 'ogacl_network_P2', 'ogacl_network_P1'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'ip access-list extended ogacl_policy_in',
                'permit ip object-group ogacl_network_P2 object-group ogacl_network_P1'
            ],)
        )