from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import unconfigure_ipv4_ogacl

class TestUnconfigureIpv4Ogacl(TestCase):

    def test_unconfigure_ipv4_ogacl(self):
        device = Mock()
        result = unconfigure_ipv4_ogacl(device, 'ogacl_policy_in')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip access-list extended ogacl_policy_in',)
        )