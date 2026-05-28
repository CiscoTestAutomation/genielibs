import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    config_load_interval_on_interface,
)


class TestConfigLoadIntervalOnInterface(TestCase):

    def test_config_load_interval_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_load_interval_on_interface(
            device,
            "Fou2/0/20",
            "300",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Fou2/0/20", sent_commands)
        self.assertIn("load-interval 300", sent_commands)


if __name__ == "__main__":
    unittest.main()