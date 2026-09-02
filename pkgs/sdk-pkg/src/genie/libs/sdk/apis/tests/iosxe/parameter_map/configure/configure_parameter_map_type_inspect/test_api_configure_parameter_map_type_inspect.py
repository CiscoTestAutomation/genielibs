from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.parameter_map.configure import (
    configure_parameter_map_type_inspect,
)


class TestConfigureParameterMapTypeInspect(TestCase):

    def test_configure_parameter_map_type_inspect(self):
        self.device = Mock()
        configure_parameter_map_type_inspect(self.device, 'log_param')
        self.device.configure.assert_called_once_with(
            [
                'parameter-map type inspect log_param',
                'log dropped-packets',
            ]
        )

    def test_configure_parameter_map_type_inspect_no_log(self):
        self.device = Mock()
        configure_parameter_map_type_inspect(
            self.device, 'global', log_dropped_packets=False,
        )
        self.device.configure.assert_called_once_with(
            [
                'parameter-map type inspect global',
            ]
        )

    def test_configure_parameter_map_type_inspect_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_parameter_map_type_inspect(self.device, 'log_param')
