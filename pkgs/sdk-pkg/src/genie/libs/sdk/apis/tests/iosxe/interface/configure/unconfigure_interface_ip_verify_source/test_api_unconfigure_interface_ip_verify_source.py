import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_ip_verify_source


class TestUnconfigureInterfaceIpVerifySource(TestCase):

    def test_unconfigure_interface_ip_verify_source(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_ip_verify_source(
            device,
            "g1/0/4",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface g1/0/4",
                "no ip verify source",
            ],
        )


if __name__ == "__main__":
    unittest.main()