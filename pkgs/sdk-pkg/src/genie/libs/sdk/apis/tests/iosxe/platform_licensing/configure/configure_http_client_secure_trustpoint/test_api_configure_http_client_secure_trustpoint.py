import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_http_client_secure_trustpoint


class TestConfigureHttpClientSecureTrustpoint(unittest.TestCase):

    def test_configure_http_client_secure_trustpoint(self):
        device = Mock()

        result = configure_http_client_secure_trustpoint(
            device,
            'CISCO_IDEVID_SUDI'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip http client secure-trustpoint CISCO_IDEVID_SUDI',)
        )