from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_ip_role_based_acl
from unittest.mock import Mock


class TestConfigureIpRoleBasedAcl(TestCase):

    def test_configure_ip_role_based_acl(self):
        self.device = Mock()
        result = configure_ip_role_based_acl(self.device, 'Acl_1', 'ip', 'tcp', 'permit', None, None, None, 'src', None, None, '23', '34', '45', '67', 'dst', None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list role-based Acl_1', 'permit tcp src range 23 34 dst range 45 67'],)
        )
