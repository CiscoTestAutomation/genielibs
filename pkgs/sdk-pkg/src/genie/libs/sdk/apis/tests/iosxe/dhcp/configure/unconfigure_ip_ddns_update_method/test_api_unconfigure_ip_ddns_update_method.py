from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_ddns_update_method
from unittest.mock import Mock


class TestUnconfigureIpDdnsUpdateMethod(TestCase):

    def test_unconfigure_ip_ddns_update_method(self):
        self.device = Mock()
        result = unconfigure_ip_ddns_update_method(self.device, 'test')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip ddns update method test'],)
        )
