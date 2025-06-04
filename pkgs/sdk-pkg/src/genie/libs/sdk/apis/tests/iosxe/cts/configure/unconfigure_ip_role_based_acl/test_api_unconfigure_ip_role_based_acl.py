from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_ip_role_based_acl
from unittest.mock import Mock


class TestUnconfigureIpRoleBasedAcl(TestCase):

    def test_unconfigure_ip_role_based_acl(self):
        self.device = Mock()
        result = unconfigure_ip_role_based_acl(self.device, 'abc14','ip')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip access-list role-based abc14',)
        )

