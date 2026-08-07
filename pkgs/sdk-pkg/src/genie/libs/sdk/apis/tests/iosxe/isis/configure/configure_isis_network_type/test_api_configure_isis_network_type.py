import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import configure_isis_network_type


class TestConfigureIsisNetworkType(TestCase):

    def test_configure_isis_network_type(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isis_network_type(
            device,
            "49.0000.1720.1604.2222.00",
            None,
            None,
            None,
            "ietf",
            "wide",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "router isis",
                "net 49.0000.1720.1604.2222.00",
                "nsf ietf",
                "metric-style wide",
            ],
        )


if __name__ == "__main__":
    unittest.main()