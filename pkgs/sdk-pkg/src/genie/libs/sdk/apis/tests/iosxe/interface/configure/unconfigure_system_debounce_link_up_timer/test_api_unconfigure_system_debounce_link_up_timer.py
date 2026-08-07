import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_system_debounce_link_up_timer,
)


class TestUnconfigureSystemDebounceLinkUpTimer(TestCase):

    def test_unconfigure_system_debounce_link_up_timer(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_system_debounce_link_up_timer(
            device,
            "4000",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "no system debounce link-up 4000",
        )


if __name__ == "__main__":
    unittest.main()