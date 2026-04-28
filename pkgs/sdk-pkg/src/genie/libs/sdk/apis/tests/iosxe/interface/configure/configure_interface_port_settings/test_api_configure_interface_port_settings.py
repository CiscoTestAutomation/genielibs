from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_port_settings
from unittest.mock import Mock


class TestConfigureInterfacePortSettings(TestCase):

    def test_configure_interface_port_settings(self):
        # speed and duplex require autoneg disable
        self.device = Mock()
        configure_interface_port_settings(self.device, 'TE0/1/0', '1000', 'full', 'disable')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'port-settings speed 1000', 'port-settings duplex full', 'port-settings autoneg disable'],)
        )

    def test_configure_interface_port_settings_combined_port_settings(self):
        # combined form with autoneg disable
        self.device = Mock()
        configure_interface_port_settings(self.device, 'TE0/1/0', '1000', 'full', 'disable', combined_port_settings=True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'port-settings speed 1000 duplex full autoneg disable'],)
        )

    def test_configure_interface_port_settings_no_args_raises(self):
        self.device = Mock()
        with self.assertRaises(ValueError):
            configure_interface_port_settings(self.device, 'TE0/1/0')

    def test_configure_interface_port_settings_empty_args_raises(self):
        self.device = Mock()
        with self.assertRaises(ValueError):
            configure_interface_port_settings(self.device, 'TE0/1/0', '', '', '')

    def test_configure_interface_port_settings_speed_only(self):
        self.device = Mock()
        configure_interface_port_settings(self.device, 'TE0/1/0', speed='1000')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'port-settings speed 1000'],)
        )

    def test_configure_interface_port_settings_duplex_only(self):
        self.device = Mock()
        configure_interface_port_settings(self.device, 'TE0/1/0', duplex='full')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'port-settings duplex full'],)
        )

    def test_configure_interface_port_settings_autoneg_only(self):
        self.device = Mock()
        configure_interface_port_settings(self.device, 'TE0/1/0', autoneg='enable')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'port-settings autoneg enable'],)
        )

    def test_configure_interface_port_settings_partial_combined_port_settings(self):
        # duplex with autoneg disable in combined form
        self.device = Mock()
        configure_interface_port_settings(self.device, 'TE0/1/0', duplex='full', autoneg='disable', combined_port_settings=True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'port-settings duplex full autoneg disable'],)
        )

