from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.telemetry.configure import (
    configure_telemetry_ietf_subscription,
)


class TestConfigureTelemetryIetfSubscription(TestCase):

    def test_configure_telemetry_ietf_subscription(self):
        device = Mock()

        result = configure_telemetry_ietf_subscription(device, 501)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'telemetry ietf subscription 501'
        )
