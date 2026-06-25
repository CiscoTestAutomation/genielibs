import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import unconfigure_http_secure_trustpoint


class TestUnconfigureHttpSecureTrustpoint(unittest.TestCase):

    def test_unconfigure_http_secure_trustpoint(self):
        device = Mock()

        result = unconfigure_http_secure_trustpoint(
            device,
            'CISCO_IDEVID_SUDI'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip http secure-trustpoint CISCO_IDEVID_SUDI',)
        )