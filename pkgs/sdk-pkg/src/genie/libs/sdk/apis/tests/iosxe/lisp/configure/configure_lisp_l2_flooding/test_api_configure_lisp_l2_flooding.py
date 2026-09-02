import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lisp.configure import (
    configure_lisp_l2_flooding,
)


class TestConfigureLispL2Flooding(TestCase):

    def test_configure_lisp_l2_flooding(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_lisp_l2_flooding(
            device,
            "2",
            "110",
            "239.0.0.1",
            "arp-nd",
            "unknown-unicast",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "router lisp",
                "instance-id 2",
                "service ethernet",
                "eid-table vlan 110",
                "broadcast-underlay 239.0.0.1",
                "flood arp-nd",
                "flood unknown-unicast",
            ],
        )


if __name__ == "__main__":
    unittest.main()
