import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_ppp_multilink


class TestConfigurePppMultilink(TestCase):

    def test_configure_ppp_multilink(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ppp_multilink(
            device,
            "Dialer10",
            True,
            "hostname",
            "10",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Dialer10",
                "ppp multilink",
                "ppp multilink interleave",
                "ppp multilink endpoint hostname",
                "ppp multilink fragment delay 10",
            ],
        )


if __name__ == "__main__":
    unittest.main()