from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cat9k.c9610.configure import unconfigure_hw_module_switch_slot_shutdown
from unittest.mock import Mock


class TestUnconfigureHwModuleSwitchSlotShutdown(TestCase):

    def test_unconfigure_hw_module_switch_slot_shutdown(self):
        self.device = Mock()
        result = unconfigure_hw_module_switch_slot_shutdown(self.device, 1, 1, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no hw-module switch 1 slot 1 shutdown',)
        )
