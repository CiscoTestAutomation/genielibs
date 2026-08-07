import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_ppp_multilink


class TestUnconfigurePppMultilink(TestCase):

    def test_unconfigure_ppp_multilink(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ppp_multilink(
            device,
            "Dialer10",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface Dialer10",
            sent_commands,
        )
        self.assertIn(
            "no ppp multilink",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()