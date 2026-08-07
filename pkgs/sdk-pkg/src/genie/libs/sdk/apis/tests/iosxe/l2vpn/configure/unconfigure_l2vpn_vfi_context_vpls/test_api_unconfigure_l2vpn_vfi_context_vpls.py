import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.l2vpn.configure import (
    unconfigure_l2vpn_vfi_context_vpls,
)


class TestUnconfigureL2vpnVfiContextVpls(TestCase):

    def test_unconfigure_l2vpn_vfi_context_vpls(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_l2vpn_vfi_context_vpls(
            device,
            "10",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "no l2vpn vfi context 10",
            ],
        )


if __name__ == "__main__":
    unittest.main()
