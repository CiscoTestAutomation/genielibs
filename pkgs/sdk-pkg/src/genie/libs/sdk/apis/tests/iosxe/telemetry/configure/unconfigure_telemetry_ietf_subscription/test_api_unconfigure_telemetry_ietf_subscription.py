from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.telemetry.configure import (
    unconfigure_telemetry_ietf_subscription,
)


class TestUnconfigureTelemetryIetfSubscription(TestCase):

    def test_unconfigure_telemetry_ietf_subscription(self):
        device = Mock()

        result = unconfigure_telemetry_ietf_subscription(device, 501)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no telemetry ietf subscription 501'
        )
