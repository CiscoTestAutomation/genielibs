from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.interface.configure import (
    unconfigure_smartpower_interface_role,
)


class TestUnconfigureSmartpowerInterfaceRole(TestCase):

    def test_unconfigure_smartpower_interface_role(self):
        device = Mock()

        result = unconfigure_smartpower_interface_role(
            device,
            'Gi1/0/13',
            'critical',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ['interface Gi1/0/13', 'no smartpower role critical']
        )
