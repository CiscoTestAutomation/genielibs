from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.isg.configure import unconfigure_class_map_type_traffic


class TestUnconfigureClassMapTypeTraffic(TestCase):

    def test_unconfigure_class_map_type_traffic(self):
        self.device = Mock()
        unconfigure_class_map_type_traffic(self.device, 'Local8_TC')
        self.device.configure.assert_called_once_with(
            "no class-map type traffic match-any Local8_TC"
        )

    def test_unconfigure_class_map_type_traffic_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_class_map_type_traffic(self.device, 'Local8_TC')
