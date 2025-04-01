from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hardware.configure import unconfigure_hw_module_breakout
from unittest.mock import Mock


class TestUnconfigureHwModuleBreakout(TestCase):

    def test_unconfigure_hw_module_breakout(self):
        self.device = Mock()
        result = unconfigure_hw_module_breakout(self.device, None, None, '1', '1', '1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no hw-module breakout module 1 port 1 switch 1'],)
        )
