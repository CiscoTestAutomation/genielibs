from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.isg.configure import (
    configure_policy_map_type_service_smtp_redirect,
)


class TestConfigurePolicyMapTypeServiceSmtpRedirect(TestCase):

    def test_configure_policy_map_type_service_smtp_redirect(self):
        device = Mock()
        configure_policy_map_type_service_smtp_redirect(device)

        device.configure.assert_called_once_with([
            "policy-map type service SMTP_REDIRECT_SERVICE",
            " 15 class type traffic SMTP_REDIRECT_TC",
            "  redirect to group SMTP_REDIRECT_GROUP",
        ])

    def test_configure_policy_map_type_service_smtp_custom(self):
        device = Mock()
        configure_policy_map_type_service_smtp_redirect(
            device,
            policy_map_name='SMTP_CUSTOM_SERVICE',
            class_name='SMTP_CUSTOM_TC',
            group_name='SMTP_CUSTOM_GROUP',
            sequence=25,
        )

        device.configure.assert_called_once_with([
            "policy-map type service SMTP_CUSTOM_SERVICE",
            " 25 class type traffic SMTP_CUSTOM_TC",
            "  redirect to group SMTP_CUSTOM_GROUP",
        ])

    def test_configure_policy_map_type_service_smtp_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_policy_map_type_service_smtp_redirect(device)
