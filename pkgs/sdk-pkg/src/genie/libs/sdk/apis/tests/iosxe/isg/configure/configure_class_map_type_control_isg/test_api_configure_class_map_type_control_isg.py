from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.isg.configure import (
    configure_class_map_type_control_isg,
)


class TestConfigureClassMapTypeControlIsg(TestCase):

    def test_configure_class_map_type_control_isg_with_vlans(self):
        device = Mock()
        configure_class_map_type_control_isg(
            device,
            'SECURE_REM',
            match_type='match-any',
            matches=['match vlan 130', 'match vlan 140'],
        )

        device.configure.assert_called_once_with([
            "class-map type control match-any SECURE_REM",
            " match vlan 130",
            " match vlan 140",
        ])

    def test_configure_class_map_type_control_isg_with_remote_id(self):
        device = Mock()
        configure_class_map_type_control_isg(
            device,
            'SECURE_REM',
            matches=[
                'available remote-id',
                'match not remote-id unauthenticated',
            ],
        )

        device.configure.assert_called_once_with([
            "class-map type control match-all SECURE_REM",
            " available remote-id",
            " match not remote-id unauthenticated",
        ])

    def test_configure_class_map_type_control_isg_with_service(self):
        device = Mock()
        configure_class_map_type_control_isg(
            device,
            'DEFAULT_L4R',
            matches=['match service-name DEFAULT_L4R_REDIRECT_SERVICE'],
        )

        device.configure.assert_called_once_with([
            "class-map type control match-all DEFAULT_L4R",
            " match service-name DEFAULT_L4R_REDIRECT_SERVICE",
        ])

    def test_configure_class_map_type_control_isg_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_class_map_type_control_isg(device, 'SECURE_REM')
