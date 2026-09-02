from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.interface.configure import (
    configure_smartpower_interface_name_default,
)


class TestConfigureSmartpowerInterfaceNameDefault(TestCase):

    def test_configure_smartpower_interface_name_default(self):
        device = Mock()

        result = configure_smartpower_interface_name_default(device, 'Gi1/0/13')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface Gi1/0/13',
                'default smartpower name',
            ]
        )
