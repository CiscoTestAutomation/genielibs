import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_system_debounce_link_down_timer,
)


class TestUnconfigureSystemDebounceLinkDownTimer(TestCase):

    def test_unconfigure_system_debounce_link_down_timer(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_system_debounce_link_down_timer(
            device,
            "4000",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "no system debounce link-down 4000"
        )


if __name__ == "__main__":
    unittest.main()