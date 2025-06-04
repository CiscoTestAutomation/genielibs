from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_role_based_permission
from unittest.mock import Mock


class TestUnconfigureCtsRoleBasedPermission(TestCase):

    def test_unconfigure_cts_role_based_permission(self):
        self.device = Mock()
        result = unconfigure_cts_role_based_permission(self.device, '2900', '3300', 'ipv6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no cts role-based permissions from 2900 to 3300 ipv6',)
        )

