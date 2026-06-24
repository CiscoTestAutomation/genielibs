import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_channel_group_auto_lacp


class TestUnconfigureInterfaceChannelGroupAutoLacp(TestCase):

    def test_unconfigure_interface_channel_group_auto_lacp(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_channel_group_auto_lacp(
            device,
            "gi1/0/2",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface gi1/0/2",
                "no channel-group auto",
            ],
        )


if __name__ == "__main__":
    unittest.main()