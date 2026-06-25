import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_rep_segment_edge_preferred


class TestConfigureInterfaceRepSegmentEdgePreferred(TestCase):

    def test_configure_interface_rep_segment_edge_preferred(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_rep_segment_edge_preferred(
            device,
            "GigabitEthernet1/1",
            "1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/1", sent_commands)
        self.assertIn("switchport", sent_commands)
        self.assertIn("switchport mode trunk", sent_commands)
        self.assertIn("rep segment 1 edge preferred", sent_commands)


if __name__ == "__main__":
    unittest.main()