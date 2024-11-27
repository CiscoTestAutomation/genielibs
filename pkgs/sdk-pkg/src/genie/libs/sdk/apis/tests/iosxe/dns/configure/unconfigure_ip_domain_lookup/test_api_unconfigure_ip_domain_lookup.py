from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import unconfigure_ip_domain_lookup
from unittest.mock import Mock


class TestUnconfigureIpDomainLookup(TestCase):

    def test_unconfigure_ip_domain_lookup(self):
        self.device = Mock()
        result = unconfigure_ip_domain_lookup(self.device)
        self.device.configure.assert_called_with(['no ip domain lookup'])
