import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import unconfigure_ip_http_secure_server


class TestUnconfigureIpHttpSecureServer(unittest.TestCase):

    def test_unconfigure_ip_http_secure_server(self):
        device = Mock()

        result = unconfigure_ip_http_secure_server(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip http secure-server',)
        )