from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import unconfigure_ip_host_view
from unittest.mock import Mock


class TestUnconfigureIpHostView(TestCase):

    def test_unconfigure_ip_host_view(self):
        self.device = Mock()
        result = unconfigure_ip_host_view(self.device, 'myview', 'example.com', ['10.1.1.1', '10.1.1.2', '10.1.1.3'])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip host view myview example.com 10.1.1.1 10.1.1.2 10.1.1.3',)
        )
