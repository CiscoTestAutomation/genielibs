from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_http_resolve_hostname_ipv4_first


class TestConfigureCallHomeHttpResolveHostnameIpv4First(TestCase):

    def test_configure_call_home_http_resolve_hostname_ipv4_first(self):
        self.device = Mock()
        result = configure_call_home_http_resolve_hostname_ipv4_first(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['call-home', 'http resolve-hostname ipv4-first'],)
        )
