from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.isg.configure import configure_class_map_type_traffic


class TestConfigureClassMapTypeTraffic(TestCase):

    def test_configure_class_map_type_traffic_no_acl(self):
        self.device = Mock()
        configure_class_map_type_traffic(self.device, 'NONTC')
        self.device.configure.assert_called_once_with(
            ["class-map type traffic match-any NONTC"]
        )

    def test_configure_class_map_type_traffic_with_access_groups(self):
        self.device = Mock()
        configure_class_map_type_traffic(
            self.device, 'Local8_TC',
            access_groups=[
                {'direction': 'input', 'name': 'ACL_IN_INTERNET1'},
                {'direction': 'output', 'name': 'ACL_OUT_INTERNET1'},
            ]
        )
        self.device.configure.assert_called_once_with(
            [
                "class-map type traffic match-any Local8_TC",
                " match access-group input name ACL_IN_INTERNET1",
                " match access-group output name ACL_OUT_INTERNET1",
            ]
        )

    def test_configure_class_map_type_traffic_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_class_map_type_traffic(self.device, 'NONTC')
