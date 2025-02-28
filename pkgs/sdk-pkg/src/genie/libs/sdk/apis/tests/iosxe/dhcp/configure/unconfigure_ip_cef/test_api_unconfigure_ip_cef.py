from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_cef
from unittest.mock import Mock


class TestUnconfigureIpCef(TestCase):

    def test_unconfigure_ip_cef(self):
        self.device = Mock()
        result = unconfigure_ip_cef(self.device, 'distributed')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip cef distributed'],)
        )
