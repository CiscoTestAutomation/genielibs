from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_role_based_access_list
from unittest.mock import Mock


class TestConfigureRoleBasedAccessList(TestCase):

    def test_configure_role_based_access_list(self):
        self.device = Mock()
        result = configure_role_based_access_list(self.device, 'SGACL_V6_PERMIT', 'ipv6', 'permit')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 access-list role-based SGACL_V6_PERMIT', 'permit ipv6'],)
        )
