import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.l2vpn.configure import (
    configure_l2vpn_vfi_context_vpls,
)


class TestConfigureL2vpnVfiContextVpls(TestCase):

    def test_configure_l2vpn_vfi_context_vpls(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_l2vpn_vfi_context_vpls(
            device,
            "10",
            None,
            "True",
            "10",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "l2vpn vfi context 10",
                "vpn id 10",
                "autodiscovery bgp signaling ldp",
            ],
        )


if __name__ == "__main__":
    unittest.main()
