import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import configure_isis_interface_metric


class TestConfigureIsisInterfaceMetric(TestCase):

    def test_configure_isis_interface_metric(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isis_interface_metric(
            device,
            "Tunnel1",
            "10",
            "ipv4",
            "level-2",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Tunnel1",
                "isis metric 10 level-2",
            ],
        )


if __name__ == "__main__":
    unittest.main()