from unittest import TestCase
from genie.libs.sdk.apis.iosxe.debug.configure import debug_platform_software_fed_drop_capture
from unittest.mock import Mock


class TestDebugPlatformSoftwareFedDropCapture(TestCase):

    def test_debug_platform_software_fed_drop_capture(self):
        self.device = Mock()
        result = debug_platform_software_fed_drop_capture(self.device, 'set-trap', 'npu-trap', 'ipv6', 'ipv6-hop-limit', 'active', None)
        self.assertIsNone(result)
        self.device.execute.assert_called_with("debug platform software fed active drop-capture set-trap npu-trap ipv6 ipv6-hop-limit")
