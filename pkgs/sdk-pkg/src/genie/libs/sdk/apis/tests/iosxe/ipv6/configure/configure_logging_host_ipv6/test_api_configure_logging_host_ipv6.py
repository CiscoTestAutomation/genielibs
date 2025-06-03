from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import configure_logging_host_ipv6
from unittest.mock import Mock


class TestConfigureLoggingHostIpv6(TestCase):

    def test_configure_logging_host_ipv6(self):
        self.device = Mock()
        result = configure_logging_host_ipv6(self.device, '2001:db8::1', 'xml')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['logging host ipv6 2001:db8::1 xml'],)
        )
