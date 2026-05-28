import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_service_compress_config


class TestConfigureServiceCompressConfig(unittest.TestCase):

    def test_configure_service_compress_config(self):
        device = Mock()

        result = configure_service_compress_config(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('service compress-config',)
        )