from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_ip_acl


class TestConfigureIpAcl(TestCase):

    def test_configure_ip_acl(self):
        self.device = Mock()
        configure_ip_acl(self.device, 'racl1', 'permit', '100.1.1.2', '150.1.1.2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended racl1', 'permit ip host 100.1.1.2 host 150.1.1.2'] ,)
        )
