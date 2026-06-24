import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.l2qos.configure import (
    unconfigure_interface_switchport_priority_default,
)


class TestUnconfigureInterfaceSwitchportPriorityDefault(TestCase):

    def test_unconfigure_interface_switchport_priority_default(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_interface_switchport_priority_default(
            device, interface="GigabitEthernet1/0/1")

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            "interface GigabitEthernet1/0/1",
            "no switchport priority default",
        ])


if __name__ == "__main__":
    unittest.main()
