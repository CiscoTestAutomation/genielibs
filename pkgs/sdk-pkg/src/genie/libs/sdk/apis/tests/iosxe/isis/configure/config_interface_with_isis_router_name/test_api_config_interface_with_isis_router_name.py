import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import (
    config_interface_with_isis_router_name,
)


class TestConfigInterfaceWithIsisRouterName(TestCase):

    def test_config_interface_with_isis_router_name(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_with_isis_router_name(
            device,
            "TenGigabitEthernet5/0/45",
            "isis_1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TenGigabitEthernet5/0/45",
                "ip router isis isis_1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
