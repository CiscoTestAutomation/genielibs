import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lisp.configure import (
    configure_lisp_enhanced_forwarding,
)


class TestConfigureLispEnhancedForwarding(TestCase):

    def test_configure_lisp_enhanced_forwarding(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_lisp_enhanced_forwarding(
            device,
            "2",
            "110",
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
                "enhanced-forwarding",
            ],
        )


if __name__ == "__main__":
    unittest.main()
