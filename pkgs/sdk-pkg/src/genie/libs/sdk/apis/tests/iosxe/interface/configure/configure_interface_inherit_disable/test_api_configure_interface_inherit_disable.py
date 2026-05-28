import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_inherit_disable,
)


class TestConfigureInterfaceInheritDisable(TestCase):

    def test_configure_interface_inherit_disable(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_inherit_disable(
            device,
            "te1/0/6",
            "interface-template-sticky",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface te1/0/6", sent_commands)
        self.assertIn(
            "access-session inherit disable interface-template-sticky",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()