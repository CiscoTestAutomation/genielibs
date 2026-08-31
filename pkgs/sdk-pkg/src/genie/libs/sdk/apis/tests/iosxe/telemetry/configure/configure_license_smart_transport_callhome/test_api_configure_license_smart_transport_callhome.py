from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.telemetry.configure import (
    configure_license_smart_transport_callhome,
)


class TestConfigureLicenseSmartTransportCallhome(TestCase):

    def test_configure_license_smart_transport_callhome(self):
        device = Mock()

        result = configure_license_smart_transport_callhome(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'license smart transport callhome'
        )
