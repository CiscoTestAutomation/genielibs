from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.isg.configure import (
    configure_policy_map_type_service_https_l4r_redirect,
)


class TestConfigurePolicyMapTypeServiceHttpsL4rRedirect(TestCase):

    def test_configure_policy_map_type_service_https_l4r_redirect(self):
        device = Mock()
        configure_policy_map_type_service_https_l4r_redirect(device)

        device.configure.assert_called_once_with([
            "policy-map type service HTTPS_L4R_REDIRECT_SERVICE",
            " 25 class type traffic HTTPS_L4R_REDIRECT_TC",
            "  redirect to group HTTPS_L4R_REDIRECT_GROUP",
        ])

    def test_configure_policy_map_type_service_https_l4r_custom(self):
        device = Mock()
        configure_policy_map_type_service_https_l4r_redirect(
            device,
            policy_map_name='HTTPS_CUSTOM_SERVICE',
            class_name='HTTPS_CUSTOM_TC',
            group_name='HTTPS_CUSTOM_GROUP',
            sequence=30,
        )

        device.configure.assert_called_once_with([
            "policy-map type service HTTPS_CUSTOM_SERVICE",
            " 30 class type traffic HTTPS_CUSTOM_TC",
            "  redirect to group HTTPS_CUSTOM_GROUP",
        ])

    def test_configure_policy_map_type_service_https_l4r_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_policy_map_type_service_https_l4r_redirect(device)
