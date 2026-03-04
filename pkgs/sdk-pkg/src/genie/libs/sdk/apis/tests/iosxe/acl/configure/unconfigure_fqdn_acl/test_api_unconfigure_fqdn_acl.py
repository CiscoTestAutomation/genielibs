from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_fqdn_acl
from unittest.mock import Mock


class TestUnconfigureFqdnAcl(TestCase):

    def test_unconfigure_fqdn_acl(self):
        self.device = Mock()
        result = unconfigure_fqdn_acl(self.device, 'FQDN1', 'ip')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip access-list fqdn FQDN1',)
        )
