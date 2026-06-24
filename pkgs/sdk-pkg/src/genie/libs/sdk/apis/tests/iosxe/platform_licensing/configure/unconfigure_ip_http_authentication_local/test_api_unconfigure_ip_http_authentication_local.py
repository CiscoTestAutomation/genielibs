import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import unconfigure_ip_http_authentication_local


class TestUnconfigureIpHttpAuthenticationLocal(unittest.TestCase):

    def test_unconfigure_ip_http_authentication_local(self):
        device = Mock()

        result = unconfigure_ip_http_authentication_local(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip http authentication local',)
        )