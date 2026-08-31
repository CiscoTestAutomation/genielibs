from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.isg.configure import (
    configure_policy_map_type_service_opengarden,
)


class TestConfigurePolicyMapTypeServiceOpengarden(TestCase):

    def test_configure_policy_map_type_service_opengarden(self):
        device = Mock()
        configure_policy_map_type_service_opengarden(device)

        device.configure.assert_called_once_with([
            "policy-map type service OPENGARDEN_SERVICE",
            " 10 class type traffic OPENGARDEN_TC",
            " class type traffic default input",
            "  drop",
        ])

    def test_configure_policy_map_type_service_opengarden_custom(self):
        device = Mock()
        configure_policy_map_type_service_opengarden(
            device,
            policy_map_name='OPEN_SERVICE',
            class_name='OPEN_TC',
            sequence=20,
            default_direction='in-out',
        )

        device.configure.assert_called_once_with([
            "policy-map type service OPEN_SERVICE",
            " 20 class type traffic OPEN_TC",
            " class type traffic default in-out",
            "  drop",
        ])

    def test_configure_policy_map_type_service_opengarden_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_policy_map_type_service_opengarden(device)
