import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_ip_http_authentication_local


class TestConfigureIpHttpAuthenticationLocal(unittest.TestCase):

    def test_configure_ip_http_authentication_local(self):
        device = Mock()

        result = configure_ip_http_authentication_local(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip http authentication local',)
        )