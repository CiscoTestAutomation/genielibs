from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_http_proxy


class TestConfigureCallHomeHttpProxy(TestCase):

    def test_configure_call_home_http_proxy(self):
        self.device = Mock()
        result = configure_call_home_http_proxy(self.device, 'test', '1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['call-home', 'http-proxy test port 1'],)
        )
