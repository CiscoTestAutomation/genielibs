import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.l2qos.configure import (
    configure_interface_switchport_priority_extend_cos,
)


class TestConfigureInterfaceSwitchportPriorityExtendCos(TestCase):

    def test_configure_interface_switchport_priority_extend_cos(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_interface_switchport_priority_extend_cos(
            device, interface="GigabitEthernet1/0/1", cos=3)

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            "interface GigabitEthernet1/0/1",
            "switchport priority extend cos 3",
        ])


if __name__ == "__main__":
    unittest.main()
