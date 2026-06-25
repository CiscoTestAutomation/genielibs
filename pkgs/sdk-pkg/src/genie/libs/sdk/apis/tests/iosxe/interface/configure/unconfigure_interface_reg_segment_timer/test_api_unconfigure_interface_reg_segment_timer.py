import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_reg_segment_timer


class TestUnconfigureInterfaceRegSegmentTimer(TestCase):

    def test_unconfigure_interface_reg_segment_timer(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_reg_segment_timer(
            device,
            "Gi1/0/3",
            "2000",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Gi1/0/3",
                "no rep lsl-age-timer 2000",
            ],
        )


if __name__ == "__main__":
    unittest.main()