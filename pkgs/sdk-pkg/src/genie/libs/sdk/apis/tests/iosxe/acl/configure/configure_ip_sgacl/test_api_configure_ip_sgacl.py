from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_ip_sgacl


class TestConfigureIpSgacl(TestCase):

    def test_configure_ip_sgacl(self):
        self.device = Mock()
        configure_ip_sgacl(self.device, 'permit', 'ipv6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 access-list role-based permit', 'permit ipv6 log'] ,)
        )
