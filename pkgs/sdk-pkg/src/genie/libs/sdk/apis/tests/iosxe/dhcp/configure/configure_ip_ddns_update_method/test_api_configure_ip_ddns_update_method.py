from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_ddns_update_method
from unittest.mock import Mock


class TestConfigureIpDdnsUpdateMethod(TestCase):

    def test_configure_ip_ddns_update_method(self):
        self.device = Mock()
        result = configure_ip_ddns_update_method(self.device, 'test', 'HTTP', 'add', 'test_url')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip ddns update method test', 'HTTP', 'add test_url', 'interval maximum 0 1 0 0'],)
        )
