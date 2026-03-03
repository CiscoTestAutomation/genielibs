from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import unconfigure_ip_dns_view_list
from unittest.mock import Mock


class TestUnconfigureIpDnsViewList(TestCase):

    def test_unconfigure_ip_dns_view_list(self):
        self.device = Mock()
        result = unconfigure_ip_dns_view_list(self.device, 'view_list1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip dns view-list view_list1',)
        )
