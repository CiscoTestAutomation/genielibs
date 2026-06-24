import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfig_interface_prpchannel


class TestUnconfigInterfacePrpchannel(TestCase):

    def test_unconfig_interface_prpchannel(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_prpchannel(
            device,
            1,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "no interface prp-channel 1",
            ],
        )


if __name__ == "__main__":
    unittest.main()