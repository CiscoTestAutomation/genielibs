import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import configure_isis_network_entity


class TestConfigureIsisNetworkEntity(TestCase):

    def test_configure_isis_network_entity(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isis_network_entity(
            device,
            "49.0001.1111.1111.1111.00",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "router isis",
                "net 49.0001.1111.1111.1111.00",
            ],
        )


if __name__ == "__main__":
    unittest.main()