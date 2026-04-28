from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_ip_fqdn_acl
from unittest.mock import Mock


class TestUnconfigureIpFqdnAcl(TestCase):

    def test_unconfigure_ip_fqdn_acl(self):
        self.device = Mock()
        result = unconfigure_ip_fqdn_acl(self.device, 'ip', 'test', 'tcp', '10.10.10.1', '11.11.11.1', 'permit', '10', 'True', False, 'True', 'www.test', None, None, None, None, None, None, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (('ip access-list fqdn test\n'
 'no 10 permit tcp host 10.10.10.1 host dynamic 11.11.11.1 '),)
        )
