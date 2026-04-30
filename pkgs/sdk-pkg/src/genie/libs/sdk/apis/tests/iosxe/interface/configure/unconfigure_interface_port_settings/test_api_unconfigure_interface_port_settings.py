from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_port_settings
from unittest.mock import Mock


class TestUnconfigureInterfacePortSettings(TestCase):

    def test_unconfigure_interface_port_settings(self):
        # speed and duplex were configured with autoneg disable
        self.device = Mock()
        unconfigure_interface_port_settings(self.device, 'TE0/1/0', '1000', 'full', 'disable')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'no port-settings speed 1000', 'no port-settings duplex full', 'no port-settings autoneg disable'],)
        )

    def test_unconfigure_interface_port_settings_combined_port_settings(self):
        # combined form with autoneg disable
        self.device = Mock()
        unconfigure_interface_port_settings(self.device, 'TE0/1/0', '1000', 'full', 'disable', combined_port_settings=True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'no port-settings speed 1000 duplex full autoneg disable'],)
        )

    def test_unconfigure_interface_port_settings_no_args_raises(self):
        self.device = Mock()
        with self.assertRaises(ValueError):
            unconfigure_interface_port_settings(self.device, 'TE0/1/0')

    def test_unconfigure_interface_port_settings_empty_args_raises(self):
        self.device = Mock()
        with self.assertRaises(ValueError):
            unconfigure_interface_port_settings(self.device, 'TE0/1/0', '', '', '')

    def test_unconfigure_interface_port_settings_autoneg_only(self):
        self.device = Mock()
        unconfigure_interface_port_settings(self.device, 'TE0/1/0', autoneg='enable')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'no port-settings autoneg enable'],)
        )

    def test_unconfigure_interface_port_settings_speed_only(self):
        self.device = Mock()
        unconfigure_interface_port_settings(self.device, 'TE0/1/0', speed='1000')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'no port-settings speed 1000'],)
        )

    def test_unconfigure_interface_port_settings_duplex_only(self):
        self.device = Mock()
        unconfigure_interface_port_settings(self.device, 'TE0/1/0', duplex='full')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'no port-settings duplex full'],)
        )

    def test_unconfigure_interface_port_settings_partial_combined_port_settings(self):
        # duplex with autoneg disable in combined form
        self.device = Mock()
        unconfigure_interface_port_settings(self.device, 'TE0/1/0', duplex='full', autoneg='disable', combined_port_settings=True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TE0/1/0', 'no port-settings duplex full autoneg disable'],)
        )

