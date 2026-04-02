from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_ipv4_ogacl_ip

class TestConfigureIpv4OgaclIp(TestCase):

    def test_configure_ipv4_ogacl_ip(self):
        device = Mock()
        result = configure_ipv4_ogacl_ip(device, 'ogacl_policy_in', 'deny', 'any', 'any')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'ip access-list extended ogacl_policy_in',
                'deny ip any any'
            ],)
        )