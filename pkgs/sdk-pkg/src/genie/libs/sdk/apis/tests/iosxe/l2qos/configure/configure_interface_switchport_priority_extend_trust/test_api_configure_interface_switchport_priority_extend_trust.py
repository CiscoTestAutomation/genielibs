import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.l2qos.configure import (
    configure_interface_switchport_priority_extend_trust,
)


class TestConfigureInterfaceSwitchportPriorityExtendTrust(TestCase):

    def test_configure_interface_switchport_priority_extend_trust(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_interface_switchport_priority_extend_trust(
            device, interface="GigabitEthernet1/0/1")

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            "interface GigabitEthernet1/0/1",
            "switchport priority extend trust",
        ])


if __name__ == "__main__":
    unittest.main()
