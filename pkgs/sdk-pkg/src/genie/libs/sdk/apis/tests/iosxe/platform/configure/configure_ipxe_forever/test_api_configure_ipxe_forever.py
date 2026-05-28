import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ipxe_forever


class TestConfigureIpxeForever(unittest.TestCase):

    def test_configure_ipxe_forever(self):
        device = Mock()

        result = configure_ipxe_forever(device, 2)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('boot ipxe forever switch 2',)
        )