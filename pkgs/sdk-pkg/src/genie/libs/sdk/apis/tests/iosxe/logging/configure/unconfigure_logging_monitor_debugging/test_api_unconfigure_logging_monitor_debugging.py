import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.logging.configure import (
    unconfigure_logging_monitor_debugging,
)


class TestUnconfigureLoggingMonitorDebugging(unittest.TestCase):

    def test_unconfigure_logging_monitor_debugging(self):
        device = Mock()

        result = unconfigure_logging_monitor_debugging(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with("no logging monitor debugging")
