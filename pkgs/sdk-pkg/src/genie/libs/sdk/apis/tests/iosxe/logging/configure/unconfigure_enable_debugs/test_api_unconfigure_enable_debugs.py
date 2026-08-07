from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.logging.configure import unconfigure_enable_debugs


class TestUnconfigureEnableDebugs(TestCase):

    def test_unconfigure_enable_debugs(self):
        self.device = Mock()

        unconfigure_enable_debugs(self.device, log_buffer_size=1000000)

        self.device.configure.assert_called_once_with(
            [
                "no service timestamps",
                "no logging buffered debugging",
                "no logging buffered 1000000",
            ]
        )

    def test_unconfigure_enable_debugs_restore_values(self):
        self.device = Mock()

        unconfigure_enable_debugs(
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
                "no logging buffered informational",
            ]
        )

    def test_unconfigure_enable_debugs_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            unconfigure_enable_debugs(self.device, log_buffer_size=1000000)
