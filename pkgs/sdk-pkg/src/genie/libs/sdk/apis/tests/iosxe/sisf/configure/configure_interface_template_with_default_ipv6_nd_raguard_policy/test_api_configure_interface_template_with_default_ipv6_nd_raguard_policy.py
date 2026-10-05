from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sisf.configure import (
    configure_interface_template_with_default_ipv6_nd_raguard_policy,
)


class TestConfigureInterfaceTemplateWithDefaultIpv6NdRaguardPolicy(TestCase):

    def test_configure_interface_template_with_default_ipv6_nd_raguard_policy(self):
        device = Mock()
        result = (
            configure_interface_template_with_default_ipv6_nd_raguard_policy(
                device,
                'template_test',
                None,
            )
        )
        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ['template template_test', 'ipv6 nd raguard']
        )
