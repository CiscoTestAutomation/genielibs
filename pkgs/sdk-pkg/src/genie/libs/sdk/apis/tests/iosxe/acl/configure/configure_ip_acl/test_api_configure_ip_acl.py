from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_ip_acl
from unittest.mock import Mock


class TestConfigureIpAcl(TestCase):

    def test_configure_ip_acl(self):
        self.device = Mock()
        result = configure_ip_acl(self.device, 'test1', 'permit', '6.6.6.6', '7.7.7.7', 'True')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended test1', 'permit ip host 6.6.6.6 host 7.7.7.7 log'],)
        )
