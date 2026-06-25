from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.logging.configure import configure_logging
from unicon.core.errors import SubCommandFailure


class TestConfigureLogging(TestCase):

    def test_configure_logging_defaults(self):
        self.device = Mock()
        configure_logging(self.device)
        self.device.configure.assert_called_once_with(
            [
                "service timestamp",
                "no logging queue-limit",
                "no logging rate-limit",
                "logging buffer debug",
                "logging buffer 5000000",
            ]
        )

    def test_configure_logging_custom_buffer(self):
        self.device = Mock()
        configure_logging(self.device, buffer_level='informational',
                          buffer_size=10000000)
        self.device.configure.assert_called_once_with(
            [
                "service timestamp",
                "no logging queue-limit",
                "no logging rate-limit",
                "logging buffer informational",
                "logging buffer 10000000",
            ]
        )

    def test_configure_logging_no_buffer(self):
        self.device = Mock()
        configure_logging(self.device, buffer_level=None, buffer_size=None)
        self.device.configure.assert_called_once_with(
            [
                "service timestamp",
                "no logging queue-limit",
                "no logging rate-limit",
            ]
        )

    def test_configure_logging_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('Test error')
        with self.assertRaises(SubCommandFailure):
            configure_logging(self.device)
