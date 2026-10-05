from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_storm_control_level
from unittest.mock import Mock


class TestConfigureInterfaceStormControlLevel(TestCase):

    def test_configure_interface_storm_control_level(self):
        self.device = Mock()
        self.device.configure.return_value = 'ok'
        configure_interface_storm_control_level(self.device, 'Fi1/0/10', 'unicast', 7, '', '')
        self.device.configure.assert_called_once()
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Fi1/0/10', 'storm-control unicast level 7'],)
        )

    def test_configure_interface_storm_control_level_1(self):
        self.device = Mock()
        self.device.configure.return_value = 'ok'
        configure_interface_storm_control_level(self.device, 'Fi1/0/10', 'unicast', 7, 4, '')
        self.device.configure.assert_called_once()
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Fi1/0/10', 'storm-control unicast level 7 4'],)
        )

    def test_configure_interface_storm_control_level_2(self):
        self.device = Mock()
        self.device.configure.return_value = 'ok'
        configure_interface_storm_control_level(self.device, 'Fi1/0/10', 'unicast', 10000, 9990, 'bps')
        self.device.configure.assert_called_once()
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Fi1/0/10', 'storm-control unicast level bps 10000 9990'],)
        )

    def test_configure_interface_storm_control_level_3(self):
        self.device = Mock()
        self.device.configure.return_value = 'ok'
        configure_interface_storm_control_level(self.device, 'Fi1/0/10', 'multicast', 1000, 990, 'pps')
        self.device.configure.assert_called_once()
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Fi1/0/10', 'storm-control multicast level pps 1000 990'],)
        )
