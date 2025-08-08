from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_role_based_permission
from unittest.mock import Mock

class TestConfigureCtsRoleBasedPermission(TestCase):

    def test_configure_cts_role_based_permission(self):
        self.device = Mock()
        configure_cts_role_based_permission(self.device, 2900, 3300, 'ipv6', 'abcl3')
        self.assertEqual(self.device.configure.mock_calls[0].args,("cts role-based permissions from 2900 to 3300 ipv6 abcl3",))
