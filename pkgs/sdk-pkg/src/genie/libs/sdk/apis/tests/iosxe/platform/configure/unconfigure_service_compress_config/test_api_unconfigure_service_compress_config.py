import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_service_compress_config


class TestUnconfigureServiceCompressConfig(unittest.TestCase):

    def test_unconfigure_service_compress_config(self):
        device = Mock()

        result = unconfigure_service_compress_config(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no service compress-config',)
        )