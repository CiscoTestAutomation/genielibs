from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.system_integrity.configure import (
    disable_system_integrity,
)


class TestDisableSystemIntegrity(TestCase):

    def test_disable_system_integrity(self):
        device = Mock()

        result = disable_system_integrity(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no system integrity')
