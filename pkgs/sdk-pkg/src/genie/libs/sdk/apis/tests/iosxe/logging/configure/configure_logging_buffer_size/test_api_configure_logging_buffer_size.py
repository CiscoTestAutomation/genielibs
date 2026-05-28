import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.logging.configure import configure_logging_buffer_size


class TestConfigureLoggingBufferSize(unittest.TestCase):

    def test_configure_logging_buffer_size(self):
        device = Mock()

        result = configure_logging_buffer_size(device, 2147483647)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('logging buffered 2147483647')

    def test_configure_logging_buffer_size_with_severity(self):
        device = Mock()

        result = configure_logging_buffer_size(device, 1000000, 'debugging')

        self.assertIsNone(result)
        device.configure.assert_called_once_with('logging buffered 1000000 debugging')
