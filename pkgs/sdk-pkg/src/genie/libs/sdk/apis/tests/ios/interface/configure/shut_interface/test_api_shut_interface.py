from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.interface.configure import shut_interface


class TestShutInterface(TestCase):

    def test_shut_interface(self):
        self.device = Mock()
        shut_interface(self.device, 'GigabitEthernet0/0')
        self.device.configure.assert_called_once_with(
            ["interface GigabitEthernet0/0", "shutdown"]
        )

    def test_shut_interface_raises(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure("failed")
        with self.assertRaises(SubCommandFailure):
            shut_interface(self.device, 'GigabitEthernet0/0')
