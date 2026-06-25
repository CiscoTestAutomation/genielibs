import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_logging_event


class TestUnconfigureInterfaceLoggingEvent(TestCase):

    def test_unconfigure_interface_logging_event(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_logging_event(
            device,
            "Tw1/0/4",
            "link-status",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Tw1/0/4",
                "no logging event link-status",
            ],
        )


if __name__ == "__main__":
    unittest.main()