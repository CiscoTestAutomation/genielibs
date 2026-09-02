import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mcast.configure import (
    configure_pim_ssm_default,
)


class TestConfigurePimSsmDefault(TestCase):

    def test_configure_pim_ssm_default(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_pim_ssm_default(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "ip pim ssm default",
        )


if __name__ == "__main__":
    unittest.main()
