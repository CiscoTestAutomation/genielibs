from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import configure_line_vty_ipv6_access_class
from unittest.mock import Mock


class TestConfigureLineVtyIpv6AccessClass(TestCase):

    def test_configure_line_vty_ipv6_access_class(self):
        self.device = Mock()
        result = configure_line_vty_ipv6_access_class(self.device, '0', '4', 'ipv6', 'in')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['line vty 0 4', 'ipv6 access-class ipv6 in'],)
        )
