import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_smart_transport_url


class TestConfigureSmartTransportUrl(unittest.TestCase):

    def test_configure_smart_transport_url(self):
        device = Mock()

        result = configure_smart_transport_url(
            device,
            'www.test.com'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('license smart url www.test.com',)
        )