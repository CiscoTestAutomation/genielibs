from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.interface.configure import (
    configure_smartpower_interface_role,
)


class TestConfigureSmartpowerInterfaceRole(TestCase):

    def test_configure_smartpower_interface_role(self):
        device = Mock()

        result = configure_smartpower_interface_role(device, 'Gi1/0/13', 'critical')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface Gi1/0/13',
                'smartpower role critical',
            ]
        )
