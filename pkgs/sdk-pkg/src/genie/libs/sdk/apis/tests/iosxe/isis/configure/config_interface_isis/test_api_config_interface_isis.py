import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import config_interface_isis


class TestConfigInterfaceIsis(TestCase):

    def test_config_interface_isis(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_isis(
            device,
            "Tunnel1",
            "True",
            None,
            "sr",
            "1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Tunnel1",
                "ipv6 router isis sr",
                "isis ipv6 metric 1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
