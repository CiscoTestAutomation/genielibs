import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_reg_segment


class TestConfigureInterfaceRegSegment(TestCase):

    def test_configure_interface_reg_segment(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_reg_segment(
            device,
            "Gi1/0/3",
            55,
            True,
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Gi1/0/3", sent_commands)
        self.assertIn(
            "rep segment 55 edge no-neighbor preferred",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()