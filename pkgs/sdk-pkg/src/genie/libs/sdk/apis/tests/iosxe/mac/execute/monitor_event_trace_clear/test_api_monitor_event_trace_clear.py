import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mac.execute import (
    monitor_event_trace_clear,
)


class TestMonitorEventTraceClear(TestCase):

    def test_monitor_event_trace_clear(self):
        device = Mock()
        device.execute.return_value = None

        result = monitor_event_trace_clear(device, "vlan", "critical")

        self.assertIsNone(result)
        device.execute.assert_called_once()
        command = device.execute.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "monitor event-trace vlan critical clear")


if __name__ == "__main__":
    unittest.main()
