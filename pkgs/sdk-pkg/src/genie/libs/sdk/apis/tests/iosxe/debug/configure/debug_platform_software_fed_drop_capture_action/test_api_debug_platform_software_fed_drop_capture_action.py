from unittest import TestCase
from genie.libs.sdk.apis.iosxe.debug.configure import debug_platform_software_fed_drop_capture_action
from unittest.mock import Mock


class TestDebugPlatformSoftwareFedDropCaptureAction(TestCase):

    def test_debug_platform_software_fed_drop_capture_action(self):
        self.device = Mock()
        result = debug_platform_software_fed_drop_capture_action(self.device, 'clear-statistics', 'active', None)
        self.assertIsNone(result)
        self.device.execute.assert_called_with("debug platform software fed active drop-capture clear-statistics")
