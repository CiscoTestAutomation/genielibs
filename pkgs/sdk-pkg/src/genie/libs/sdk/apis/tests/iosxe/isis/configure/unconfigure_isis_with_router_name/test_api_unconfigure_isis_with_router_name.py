import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import unconfigure_isis_with_router_name


class TestUnconfigureIsisWithRouterName(TestCase):

    def test_unconfigure_isis_with_router_name(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_isis_with_router_name(device, "isis_1")

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            ["no router isis isis_1"],
        )


if __name__ == "__main__":
    unittest.main()
