import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import unconfigure_http_client_source_interface


class TestUnconfigureHttpClientSourceInterface(unittest.TestCase):

    def test_unconfigure_http_client_source_interface(self):
        device = Mock()

        result = unconfigure_http_client_source_interface(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip http client source-interface',)
        )