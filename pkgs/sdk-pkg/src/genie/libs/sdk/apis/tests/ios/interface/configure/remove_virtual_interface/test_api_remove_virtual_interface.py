from unittest import TestCase
from unittest.mock import Mock, call
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.interface.configure import remove_virtual_interface


class TestRemoveVirtualInterface(TestCase):

    def test_remove_virtual_interface_single_string(self):
        self.device = Mock()
        remove_virtual_interface(self.device, 'Loopback2')
        self.device.configure.assert_called_once_with(
            "no interface Loopback2"
        )

    def test_remove_virtual_interface_list(self):
        self.device = Mock()
        remove_virtual_interface(self.device, ['Loopback2', 'Loopback3'])
        self.device.configure.assert_has_calls([
            call("no interface Loopback2"),
            call("no interface Loopback3"),
        ])
        self.assertEqual(self.device.configure.call_count, 2)

    def test_remove_virtual_interface_raises(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure("failed")
        with self.assertRaises(SubCommandFailure):
            remove_virtual_interface(self.device, 'Loopback2')
