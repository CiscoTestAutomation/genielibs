from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.system_integrity.configure import (
    enable_system_integrity,
)


class TestEnableSystemIntegrity(TestCase):

    def test_enable_system_integrity(self):
        device = Mock()

        result = enable_system_integrity(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('system integrity')
