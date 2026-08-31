import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    unconfigure_mtc,
)


class TestUnconfigureMtc(TestCase):

    def test_unconfigure_mtc(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_mtc(
            device,
            "ipv4",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "no mgmt-traffic control ipv4",
        )


if __name__ == "__main__":
    unittest.main()
