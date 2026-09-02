import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_line_vty_needs_enhancement,
)


class TestConfigureLineVtyNeedsEnhancement(TestCase):

    def test_configure_line_vty_needs_enhancement(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_line_vty_needs_enhancement(
            device,
            0,
            4,
            0,
            0,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "line vty 0 4",
                "transport preferred ssh",
                "exec-timeout 0 0",
                "transport input ssh",
                "transport output all",
            ],
        )


if __name__ == "__main__":
    unittest.main()
