import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lldp.configure import (
    configure_lldp_tlv_select,
)


class TestConfigureLldpTlvSelect(TestCase):

    def test_configure_lldp_tlv_select(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_lldp_tlv_select(
            device,
            [
                "system-name",
                "port-vlan",
                "mac-phy-cfg",
            ],
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "lldp tlv-select system-name",
                "lldp tlv-select port-vlan",
                "lldp tlv-select mac-phy-cfg",
            ],
        )

    def test_configure_lldp_tlv_select_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_lldp_tlv_select(
            device,
            "system-capabilities",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "lldp tlv-select system-capabilities",
            ],
        )


if __name__ == "__main__":
    unittest.main()
