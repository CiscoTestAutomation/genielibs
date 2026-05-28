import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_http_client_source_interface


class TestConfigureIpHttpClientSourceInterface(unittest.TestCase):

    def test_configure_ip_http_client_source_interface(self):
        device = Mock()

        result = configure_ip_http_client_source_interface(device, 'BDI', '10')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (('ip http client source-interface BDI 10',),)
        )