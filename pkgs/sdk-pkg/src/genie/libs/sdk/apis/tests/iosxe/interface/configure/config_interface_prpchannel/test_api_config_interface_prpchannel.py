import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import config_interface_prpchannel


class TestConfigInterfacePrpchannel(TestCase):

    def test_config_interface_prpchannel(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_prpchannel(
            device,
            "GigabitEthernet1/0/21",
            1,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/21", sent_commands)
        self.assertIn("prp-channel-group 1", sent_commands)


if __name__ == "__main__":
    unittest.main()