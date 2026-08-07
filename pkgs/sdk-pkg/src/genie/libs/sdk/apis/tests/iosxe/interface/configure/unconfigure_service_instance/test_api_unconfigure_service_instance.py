import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_service_instance,
)


class TestUnconfigureServiceInstance(TestCase):

    def test_unconfigure_service_instance(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_service_instance(
            device,
            "GigabitEthernet0/0/0",
            "30",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface GigabitEthernet0/0/0",
            sent_commands,
        )
        self.assertIn(
            "no service instance 30 ethernet",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()