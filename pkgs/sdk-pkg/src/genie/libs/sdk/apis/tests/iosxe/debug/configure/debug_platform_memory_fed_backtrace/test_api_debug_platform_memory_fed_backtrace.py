from unittest import TestCase
from genie.libs.sdk.apis.iosxe.debug.configure import debug_platform_memory_fed_backtrace
from unittest.mock import Mock


class TestDebugPlatformMemoryFedBacktrace(TestCase):

    def test_debug_platform_memory_fed_backtrace(self):
        self.device = Mock()
        result = debug_platform_memory_fed_backtrace(self.device, 'stop', '1', None, None, 10)
        self.assertIsNone(result)
        self.device.execute.assert_called_with("debug platform software memory fed switch 1 alloc backtrace stop")
