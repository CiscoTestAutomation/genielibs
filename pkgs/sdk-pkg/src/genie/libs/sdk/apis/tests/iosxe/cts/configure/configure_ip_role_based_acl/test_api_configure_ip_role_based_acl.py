from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_ip_role_based_acl
from unittest.mock import Mock

class TestConfigureIpRoleBasedAcl(TestCase):

    def test_configure_ip_role_based_acl(self):
        self.device = Mock()
        configure_ip_role_based_acl(self.device, 'abc14', 'ip', 'ip', 'permit', 'log', '', '', '', '', '', '', '')
        self.assertEqual(self.device.configure.mock_calls[0].args,(['ip access-list role-based abc14', 'permit ip log'],))
