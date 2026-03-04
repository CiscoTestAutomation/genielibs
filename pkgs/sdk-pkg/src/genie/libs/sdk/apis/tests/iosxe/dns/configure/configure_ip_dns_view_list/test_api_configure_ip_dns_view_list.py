from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import configure_ip_dns_view_list
from unittest.mock import Mock


class TestConfigureIpDnsViewList(TestCase):

    def test_configure_ip_dns_view_list(self):
        self.device = Mock()
        result = configure_ip_dns_view_list(self.device, 'view_list1', 'view1', False, '3', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip dns view-list view_list1', 'view view1 3'],)
        )
