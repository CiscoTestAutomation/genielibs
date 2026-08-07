import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_vfi


class TestUnconfigureVfi(TestCase):

    def test_unconfigure_vfi(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_vfi(
            device,
            50,
            "vpls1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface vlan 50",
                "no member vfi vpls1",
            ],
        )


if __name__ == "__main__":
    unittest.main()