from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.interface.configure import unshut_interface


class TestUnshutInterface(TestCase):

    def test_unshut_interface(self):
        self.device = Mock()
        unshut_interface(self.device, 'GigabitEthernet0/0')
        self.device.configure.assert_called_once_with(
            ["interface GigabitEthernet0/0", "no shutdown"]
        )

    def test_unshut_interface_raises(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure("failed")
        with self.assertRaises(SubCommandFailure):
            unshut_interface(self.device, 'GigabitEthernet0/0')
