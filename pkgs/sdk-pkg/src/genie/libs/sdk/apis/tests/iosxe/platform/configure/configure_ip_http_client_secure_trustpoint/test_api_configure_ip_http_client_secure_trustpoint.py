import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_http_client_secure_trustpoint


class TestConfigureIpHttpClientSecureTrustpoint(unittest.TestCase):

    def test_configure_ip_http_client_secure_trustpoint(self):
        device = Mock()

        result = configure_ip_http_client_secure_trustpoint(device, 'SLA-TrustPoint')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip http client secure-trustpoint SLA-TrustPoint',)
        )