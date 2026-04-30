from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import default_interface_port_settings
from unittest.mock import Mock


class TestDefaultInterfacePortSettings(TestCase):

    def test_default_interface_port_settings(self):
        self.device = Mock()
        default_interface_port_settings(self.device, 'TE0/1/0', True, True, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'default port-settings speed', 'default port-settings duplex', 'default port-settings autoneg'],)
        )

    def test_default_interface_port_settings_combined_port_settings(self):
        self.device = Mock()
        default_interface_port_settings(self.device, 'TE0/1/0', True, True, True, combined_port_settings=True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'default port-settings speed duplex autoneg'],)
        )

    def test_default_interface_port_settings_no_args_raises(self):
        self.device = Mock()
        with self.assertRaises(ValueError):
            default_interface_port_settings(self.device, 'TE0/1/0')

    def test_default_interface_port_settings_empty_args_raises(self):
        self.device = Mock()
        with self.assertRaises(ValueError):
            default_interface_port_settings(self.device, 'TE0/1/0', False, False, False)

    def test_default_interface_port_settings_autoneg_only(self):
        self.device = Mock()
        default_interface_port_settings(self.device, 'TE0/1/0', autoneg=True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'default port-settings autoneg'],)
        )

    def test_default_interface_port_settings_speed_only(self):
        self.device = Mock()
        default_interface_port_settings(self.device, 'TE0/1/0', speed=True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'default port-settings speed'],)
        )

    def test_default_interface_port_settings_duplex_only(self):
        self.device = Mock()
        default_interface_port_settings(self.device, 'TE0/1/0', duplex=True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'default port-settings duplex'],)
        )

    def test_default_interface_port_settings_partial_combined_port_settings(self):
        self.device = Mock()
        default_interface_port_settings(self.device, 'TE0/1/0', duplex=True, autoneg=True, combined_port_settings=True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'default port-settings duplex autoneg'],)
        )

