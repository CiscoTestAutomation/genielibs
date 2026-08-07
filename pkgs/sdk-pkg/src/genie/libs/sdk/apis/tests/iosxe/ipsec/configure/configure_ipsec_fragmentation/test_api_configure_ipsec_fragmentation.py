import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ipsec_fragmentation


class TestConfigureIpsecFragmentation(TestCase):

    def test_configure_ipsec_fragmentation(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipsec_fragmentation(
            device,
            True,
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            ["crypto ipsec fragmentation after-encryption"],
        )


if __name__ == "__main__":
    unittest.main()