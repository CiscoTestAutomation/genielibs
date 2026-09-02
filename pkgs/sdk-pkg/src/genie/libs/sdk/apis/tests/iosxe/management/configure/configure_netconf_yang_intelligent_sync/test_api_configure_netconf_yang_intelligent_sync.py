import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_netconf_yang_intelligent_sync,
)


class TestConfigureNetconfYangIntelligentSync(TestCase):

    def test_configure_netconf_yang_intelligent_sync(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_netconf_yang_intelligent_sync(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "netconf-yang cisco-ia intelligent-sync",
        )


if __name__ == "__main__":
    unittest.main()
