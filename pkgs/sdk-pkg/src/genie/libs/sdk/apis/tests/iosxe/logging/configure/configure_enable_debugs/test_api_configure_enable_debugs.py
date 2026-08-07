from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.logging.configure import configure_enable_debugs


class TestConfigureEnableDebugs(TestCase):

    def test_configure_enable_debugs(self):
        self.device = Mock()

        configure_enable_debugs(self.device, log_buffer_size=1000000)

        self.device.configure.assert_called_once_with(
            [
                "service timestamps",
                "no logging queue-limit",
                "no logging rate-limit",
                "logging buffered debugging",
                "logging buffered 1000000",
            ]
        )

    def test_configure_enable_debugs_modular_options(self):
        self.device = Mock()

        configure_enable_debugs(
            self.device,
            log_buffer_size=None,
            timestamp=False,
            queue_limit=1024,
            rate_limit=100,
            buffer_level='informational',
        )

        self.device.configure.assert_called_once_with(
            [
                "logging queue-limit 1024",
                "logging rate-limit 100",
                "logging buffered informational",
            ]
        )

    def test_configure_enable_debugs_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            configure_enable_debugs(self.device, log_buffer_size=1000000)
