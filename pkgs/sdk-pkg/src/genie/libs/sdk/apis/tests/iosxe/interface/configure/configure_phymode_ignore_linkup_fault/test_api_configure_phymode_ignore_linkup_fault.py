import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_phymode_ignore_linkup_fault,
)


class TestConfigurePhymodeIgnoreLinkupFault(TestCase):

    def test_configure_phymode_ignore_linkup_fault(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_phymode_ignore_linkup_fault(
            device,
            "Hun2/0/7",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Hun2/0/7", sent_commands)
        self.assertIn("phymode ignore-linkup-fault", sent_commands)


if __name__ == "__main__":
    unittest.main()