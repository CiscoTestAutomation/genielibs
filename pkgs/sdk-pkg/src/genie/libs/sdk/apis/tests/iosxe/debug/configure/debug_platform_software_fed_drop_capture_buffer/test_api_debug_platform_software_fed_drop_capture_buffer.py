from unittest import TestCase
from genie.libs.sdk.apis.iosxe.debug.configure import debug_platform_software_fed_drop_capture_buffer
from unittest.mock import Mock


class TestDebugPlatformSoftwareFedDropCaptureBuffer(TestCase):

    def test_debug_platform_software_fed_drop_capture_buffer(self):
        self.device = Mock()
        result = debug_platform_software_fed_drop_capture_buffer(self.device, 1024, None, None)
        self.assertIsNone(result)
        self.device.execute.assert_called_with("debug platform software fed active drop-capture buffer limit 1024")
