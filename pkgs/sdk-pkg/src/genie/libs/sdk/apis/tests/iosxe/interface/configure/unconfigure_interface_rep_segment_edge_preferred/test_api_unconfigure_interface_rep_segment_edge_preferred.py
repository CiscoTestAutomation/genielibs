import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_reg_segment


class TestUnconfigureInterfaceRegSegment(TestCase):

    def test_unconfigure_interface_reg_segment_edge_preferred(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_reg_segment(
            device,
            "GigabitEthernet1/1",
            1,
            False,
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet1/1",
                "no rep segment 1 preferred",
            ],
        )


if __name__ == "__main__":
    unittest.main()