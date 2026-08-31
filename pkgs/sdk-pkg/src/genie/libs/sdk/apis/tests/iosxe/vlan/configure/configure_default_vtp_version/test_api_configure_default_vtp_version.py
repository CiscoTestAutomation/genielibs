from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_default_vtp_version,
)


class TestConfigureDefaultVtpVersion(TestCase):

    def test_configure_default_vtp_version(self):
        device = Mock()

        result = configure_default_vtp_version(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('default vtp version')
