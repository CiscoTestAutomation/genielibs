import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import configure_interface_isis_network


class TestConfigureInterfaceIsisNetwork(TestCase):

    def test_configure_interface_isis_network(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_isis_network(
            device,
            "Gi1/0/20",
            "point-to-point",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Gi1/0/20",
                "isis network point-to-point",
            ],
        )


if __name__ == "__main__":
    unittest.main()
