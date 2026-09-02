from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_interface_vtp,
)


class TestConfigureInterfaceVtp(TestCase):

    def test_configure_interface_vtp(self):
        device = Mock()

        result = configure_interface_vtp(device, 'te1/0/5')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface te1/0/5',
                'vtp',
            ]
        )
