import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.macsec.configure import (
    configure_disable_sci_dot1q_clear,
)


class TestConfigureDisableSciDot1qClear(TestCase):

    def test_configure_disable_sci_dot1q_clear(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_disable_sci_dot1q_clear(
            device,
            "Te0/1/1",
            True,
            True,
            1,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Te0/1/1",
                "macsec disable-sci",
                "macsec dot1q-in-clear 1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
