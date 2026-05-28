from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.dns.configure import configure_ip_domain_lookup


class TestConfigureIpDomainLookup(TestCase):

    def test_configure_ip_domain_lookup(self):
        self.device = Mock()
        configure_ip_domain_lookup(self.device)
        self.device.configure.assert_called_once_with(
            "ip domain lookup"
        )

    def test_configure_ip_domain_lookup_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_ip_domain_lookup(self.device)
