import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_eapol_eth_type_interface


class TestUnconfigureEapolEthTypeInterface(TestCase):

    def test_unconfigure_eapol_eth_type_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_eapol_eth_type_interface(
            device,
            "GigabitEthernet1/0/10",
            "876F",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet1/0/10",
                "no eapol eth-type 876F",
            ],
        )


if __name__ == "__main__":
    unittest.main()