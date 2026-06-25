from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.logging.configure import unconfigure_logging
from unicon.core.errors import SubCommandFailure


class TestUnconfigureLogging(TestCase):

    def test_unconfigure_logging_defaults(self):
        self.device = Mock()
        unconfigure_logging(self.device)
        self.device.configure.assert_called_once_with(
            [
                "no service timestamp",
                "logging queue-limit",
                "logging rate-limit",
                "no logging buffer debug",
                "no logging buffer 5000000",
            ]
        )

    def test_unconfigure_logging_no_buffer(self):
        self.device = Mock()
        unconfigure_logging(self.device, buffer_level=None, buffer_size=None)
        self.device.configure.assert_called_once_with(
            [
                "no service timestamp",
                "logging queue-limit",
                "logging rate-limit",
            ]
        )

    def test_unconfigure_logging_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('Test error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_logging(self.device)
