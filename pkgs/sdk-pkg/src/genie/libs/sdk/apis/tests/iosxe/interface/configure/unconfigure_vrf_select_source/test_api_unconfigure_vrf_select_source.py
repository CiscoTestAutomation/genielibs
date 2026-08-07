import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_vrf_select_source,
)


class TestUnconfigureVrfSelectSource(TestCase):

    def test_unconfigure_vrf_select_source(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_vrf_select_source(
            device,
            "Vlan100",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Vlan100",
                "no ip vrf select source",
            ],
        )


if __name__ == "__main__":
    unittest.main()