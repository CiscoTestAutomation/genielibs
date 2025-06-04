from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_role_based_permission_default
from unittest.mock import Mock


class TestUnconfigureCtsRoleBasedPermissionDefault(TestCase):

    def test_unconfigure_cts_role_based_permission_default(self):
        self.device = Mock()
        result = unconfigure_cts_role_based_permission_default(self.device, 'ipv6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no cts role-based permissions default ipv6',)
        )

