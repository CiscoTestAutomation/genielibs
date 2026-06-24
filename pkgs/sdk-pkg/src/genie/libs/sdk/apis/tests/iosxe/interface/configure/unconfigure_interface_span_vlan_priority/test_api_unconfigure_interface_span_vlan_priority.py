import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_span_vlan_priority


class TestUnconfigureInterfaceSpanVlanPriority(TestCase):

    def test_unconfigure_interface_span_vlan_priority(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_span_vlan_priority(
            device,
            "Tw1/0/10",
            100,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Tw1/0/10",
                "no spanning-tree vlan 100 priority",
            ],
        )


if __name__ == "__main__":
    unittest.main()