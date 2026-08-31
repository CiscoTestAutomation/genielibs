from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.telemetry.configure import (
    configure_license_smart_transport_smart,
)


class TestConfigureLicenseSmartTransportSmart(TestCase):

    def test_configure_license_smart_transport_smart(self):
        device = Mock()

        result = configure_license_smart_transport_smart(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'license smart transport smart'
        )
