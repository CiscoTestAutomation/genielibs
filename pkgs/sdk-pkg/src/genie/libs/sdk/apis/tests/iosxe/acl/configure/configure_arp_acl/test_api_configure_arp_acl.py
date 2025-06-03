from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_arp_acl


class TestConfigureArpAcl(TestCase):

    def test_configure_arp_acl(self):
        self.device = Mock()
        configure_arp_acl(self.device, 'test1', 'permit', '2.2.2.2', '6.6.6', '5.5.5', '', 'log')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['arp access-list test1', 'permit ip host 2.2.2.2 mac 6.6.6 5.5.5 log'],)
        )
