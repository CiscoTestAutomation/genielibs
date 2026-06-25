import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interfaces_on_port_channel


class TestUnconfigureInterfacesOnPortChannel(TestCase):

    def test_unconfigure_interfaces_on_port_channel(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interfaces_on_port_channel(
            device,
            ["HundredGigE1/0/34"],
            "desirable",
            1,
            None,
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface HundredGigE1/0/34\nno shutdown\nno channel-group 1 mode desirable\n",
        )


if __name__ == "__main__":
    unittest.main()