from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_role_based_permission_default
from unittest.mock import Mock

class TestConfigureCtsRoleBasedPermissionDefault(TestCase):

    def test_configure_cts_role_based_permission_default(self):
        self.device = Mock()
        configure_cts_role_based_permission_default(self.device, 'ipv6', 'abcl3')
        self.assertEqual(self.device.configure.mock_calls[0].args,("cts role-based permissions default ipv6 abcl3",))

