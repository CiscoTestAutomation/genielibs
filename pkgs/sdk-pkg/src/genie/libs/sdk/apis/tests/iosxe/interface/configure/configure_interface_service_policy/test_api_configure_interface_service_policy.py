import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_service_policy


class TestConfigureInterfaceServicePolicy(TestCase):

    def test_configure_interface_service_policy(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_service_policy(
            device,
            "Te0/1/0",
            "grandparent",
            "out",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Te0/1/0", sent_commands)
        self.assertIn("service-policy out grandparent", sent_commands)


if __name__ == "__main__":
    unittest.main()