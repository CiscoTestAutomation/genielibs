import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import unconfigure_ip_http_server


class TestUnconfigureIpHttpServer(unittest.TestCase):

    def test_unconfigure_ip_http_server(self):
        device = Mock()

        result = unconfigure_ip_http_server(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip http server',)
        )