import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_span_monitor_session,
)


class TestUnconfigureSpanMonitorSession(TestCase):

    def test_unconfigure_span_monitor_session(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_span_monitor_session(
            device,
            1,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ["no monitor session 1"]
        )


if __name__ == "__main__":
    unittest.main()