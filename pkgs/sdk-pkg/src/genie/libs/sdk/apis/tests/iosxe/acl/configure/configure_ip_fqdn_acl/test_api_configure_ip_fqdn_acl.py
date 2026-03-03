from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_ip_fqdn_acl
from unittest.mock import Mock


class TestConfigureIpFqdnAcl(TestCase):

    def test_configure_ip_fqdn_acl(self):
        self.device = Mock()
        result = configure_ip_fqdn_acl(self.device, 'ip', 'TEST_IP_FQDN_ACL5', 'tcp', 'any', '1.1.1.1', 'deny', '20', False, False, 'True', 'True', None, None, None, None, None, 'log', None, '122')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (('ip access-list fqdn TEST_IP_FQDN_ACL5\n'
 '20 deny tcp any host dynamic 1.1.1.1 time-range 122 log '),)
        )
