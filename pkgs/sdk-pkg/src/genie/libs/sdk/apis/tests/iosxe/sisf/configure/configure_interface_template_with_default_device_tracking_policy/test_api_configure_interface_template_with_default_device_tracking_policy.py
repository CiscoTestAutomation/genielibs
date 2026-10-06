from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sisf.configure import (
    configure_interface_template_with_default_device_tracking_policy,
)

configure_default_device_tracking_policy = (
    configure_interface_template_with_default_device_tracking_policy
)


class TestConfigureInterfaceTemplateWithDefaultDeviceTrackingPolicy(TestCase):

    def test_configure_interface_template_with_default_device_tracking_policy(
        self,
    ):
        device = Mock()

        result = configure_default_device_tracking_policy(
            device,
            'template_test',
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'template template_test',
            'device-tracking',
        ])
