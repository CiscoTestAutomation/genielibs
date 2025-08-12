from unittest import TestCase
from genie.libs.sdk.apis.iosxe.debug.configure import debug_platform_memory_fed_callsite
from unittest.mock import Mock


class TestDebugPlatformMemoryFedCallsite(TestCase):

    def test_debug_platform_memory_fed_callsite(self):
        self.device = Mock()
        result = debug_platform_memory_fed_callsite(self.device, 'stop', '1', None)
        self.assertIsNone(result)
        self.device.execute.assert_called_with("debug platform software memory fed switch 1 alloc callsite stop")
