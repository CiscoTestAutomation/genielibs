import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_vrrp_version_on_device


class TestConfigureVrrpVersionOnDevice(TestCase):

    def test_configure_vrrp_version_on_device(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_vrrp_version_on_device(
            device,
            "v3",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "fhrp version vrrp v3",
            ],
        )


if __name__ == "__main__":
    unittest.main()