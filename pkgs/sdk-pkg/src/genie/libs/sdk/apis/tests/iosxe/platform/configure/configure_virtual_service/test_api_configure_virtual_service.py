import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_virtual_service


class TestConfigureVirtualService(unittest.TestCase):

    def test_configure_virtual_service(self):
        device = Mock()

        result = configure_virtual_service(device, 'UTD')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('virtual-service UTD',)
        )