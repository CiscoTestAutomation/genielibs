import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_management_gateway,
)


class TestConfigureManagementGateway(TestCase):

    def test_configure_management_gateway(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.management = {
            "gateway": {
                "ipv4": "10.29.30.1",
            },
        }
        device.execute.return_value = (
            "ip route 0.0.0.0 0.0.0.0 10.29.30.1"
        )

        result = configure_management_gateway(device)

        self.assertIsNone(result)
        device.execute.assert_called_once()

        sent_command = device.execute.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "show running-config | include ip route 0.0.0.0 0.0.0.0",
        )

        device.configure.assert_not_called()


if __name__ == "__main__":
    unittest.main()
