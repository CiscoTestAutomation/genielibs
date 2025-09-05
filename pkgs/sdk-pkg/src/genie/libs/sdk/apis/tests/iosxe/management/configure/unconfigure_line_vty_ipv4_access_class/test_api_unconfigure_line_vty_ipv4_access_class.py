from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import unconfigure_line_vty_ipv4_access_class
from unittest.mock import Mock


class TestUnconfigureLineVtyIpv4AccessClass(TestCase):

    def test_unconfigure_line_vty_ipv4_access_class(self):
        self.device = Mock()
        result = unconfigure_line_vty_ipv4_access_class(self.device, '0', '4', 'dummy', 'in', None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['line vty 0 4', 'no access-class dummy in'],)
        )
