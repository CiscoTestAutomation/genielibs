from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import configure_ip_host_view
from unittest.mock import Mock


class TestConfigureIpHostView(TestCase):

    def test_configure_ip_host_view(self):
        self.device = Mock()
        result = configure_ip_host_view(self.device, 'myview', 'example.com', ['10.1.1.1', '10.1.1.2', '10.1.1.3'])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip host view myview example.com 10.1.1.1 10.1.1.2 10.1.1.3',)
        )
