from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.parameter_map.configure import (
    unconfigure_parameter_map_type_inspect,
)


class TestUnconfigureParameterMapTypeInspect(TestCase):

    def test_unconfigure_parameter_map_type_inspect(self):
        self.device = Mock()
        unconfigure_parameter_map_type_inspect(self.device, 'log_param')
        self.device.configure.assert_called_once_with(
            [
                'no parameter-map type inspect log_param',
            ]
        )

    def test_unconfigure_parameter_map_type_inspect_log_only(self):
        self.device = Mock()
        unconfigure_parameter_map_type_inspect(
            self.device, 'log_param', log_dropped_packets=True,
            remove_parameter_map=False,
        )
        self.device.configure.assert_called_once_with(
            [
                'parameter-map type inspect log_param',
                'no log dropped-packets',
                'exit',
            ]
        )

    def test_unconfigure_parameter_map_type_inspect_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_parameter_map_type_inspect(self.device, 'log_param')
