from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_enable_http_server


class TestConfigureEnableHttpServer(TestCase):

    def test_configure_enable_http_server(self):
        device = Mock()
        result = configure_enable_http_server(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip http server',)
        )