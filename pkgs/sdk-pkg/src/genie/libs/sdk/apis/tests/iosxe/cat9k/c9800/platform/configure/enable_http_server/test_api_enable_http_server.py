from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.configure import enable_http_server


class TestEnableHttpServer(TestCase):

    def test_enable_http_server(self):
        self.device = Mock()
        result = enable_http_server(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip http server',)
        )
