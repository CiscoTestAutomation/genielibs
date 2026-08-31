import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    unconfigure_netconf_yang_polling,
)


class TestUnconfigureNetconfYangPolling(TestCase):

    def test_unconfigure_netconf_yang_polling(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_netconf_yang_polling(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "no netconf-yang cisco-odm polling-enable",
            ],
        )


if __name__ == "__main__":
    unittest.main()
