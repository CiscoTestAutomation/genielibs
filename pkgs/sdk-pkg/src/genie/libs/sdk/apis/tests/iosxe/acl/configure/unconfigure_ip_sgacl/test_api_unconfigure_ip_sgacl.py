from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_ip_sgacl


class TestUnconfigureIpSgacl(TestCase):

    def test_unconfigure_ip_sgacl(self):
        self.device = Mock()
        unconfigure_ip_sgacl(self.device, 'permit', 'ipv6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ipv6 access-list role-based permit'] ,)
        )
