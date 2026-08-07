import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lacp.configure import (
    configure_lacp_port_priority,
)


class TestConfigureLacpPortPriority(TestCase):

    def test_configure_lacp_port_priority(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_lacp_port_priority(
            device,
            "te1/0/2",
            345,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface te1/0/2",
                "lacp port-priority 345",
            ],
        )


if __name__ == "__main__":
    unittest.main()
