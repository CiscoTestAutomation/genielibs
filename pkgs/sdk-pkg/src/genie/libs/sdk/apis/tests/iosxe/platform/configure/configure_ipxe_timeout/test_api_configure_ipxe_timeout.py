import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ipxe_timeout


class TestConfigureIpxeTimeout(unittest.TestCase):

    def test_configure_ipxe_timeout(self):
        device = Mock()

        result = configure_ipxe_timeout(device, 10, 1)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('boot ipxe timeout 10 switch 1',)
        )