from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.telemetry.configure import (
    unconfigure_license_smart_transport,
)


class TestUnconfigureLicenseSmartTransport(TestCase):

    def test_unconfigure_license_smart_transport(self):
        device = Mock()

        result = unconfigure_license_smart_transport(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no license smart transport')
