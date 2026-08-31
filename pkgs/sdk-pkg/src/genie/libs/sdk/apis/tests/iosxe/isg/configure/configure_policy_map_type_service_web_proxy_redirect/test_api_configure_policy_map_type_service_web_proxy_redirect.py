from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.isg.configure import (
    configure_policy_map_type_service_web_proxy_redirect,
)


class TestConfigurePolicyMapTypeServiceWebProxyRedirect(TestCase):

    def test_configure_policy_map_type_service_web_proxy_redirect(self):
        device = Mock()
        configure_policy_map_type_service_web_proxy_redirect(device)

        device.configure.assert_called_once_with([
            "policy-map type service WEB_PROXY_REDIRECT_SERVICE",
            " 10 class type traffic WEB_PROXY_REDIRECT_TC",
            "  redirect to group WEB_PROXY_REDIRECT_GROUP",
        ])

    def test_configure_policy_map_type_service_web_proxy_custom(self):
        device = Mock()
        configure_policy_map_type_service_web_proxy_redirect(
            device,
            policy_map_name='WEB_PROXY_CUSTOM_SERVICE',
            class_name='WEB_PROXY_CUSTOM_TC',
            group_name='WEB_PROXY_CUSTOM_GROUP',
            sequence=15,
        )

        device.configure.assert_called_once_with([
            "policy-map type service WEB_PROXY_CUSTOM_SERVICE",
            " 15 class type traffic WEB_PROXY_CUSTOM_TC",
            "  redirect to group WEB_PROXY_CUSTOM_GROUP",
        ])

    def test_configure_policy_map_type_service_web_proxy_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_policy_map_type_service_web_proxy_redirect(device)
