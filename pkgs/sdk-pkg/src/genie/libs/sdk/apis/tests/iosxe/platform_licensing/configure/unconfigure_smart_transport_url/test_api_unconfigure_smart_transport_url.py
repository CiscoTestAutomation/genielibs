import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import unconfigure_smart_transport_url


class TestUnconfigureSmartTransportUrl(unittest.TestCase):

    def test_unconfigure_smart_transport_url(self):
        device = Mock()

        result = unconfigure_smart_transport_url(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no license smart url',)
        )