import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_vrrp_on_interface


class TestConfigureVrrpOnInterface(TestCase):

    def test_configure_vrrp_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_vrrp_on_interface(
            device,
            "vlan101",
            1,
            "ipv4",
            110,
            "150",
            "10.1.0.3",
            "primary",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface vlan101",
                "vrrp 1 address-family ipv4",
                "timers advertise 110",
                "priority 150",
                "address 10.1.0.3 primary",
                "exit-vrrp",
            ],
        )


if __name__ == "__main__":
    unittest.main()