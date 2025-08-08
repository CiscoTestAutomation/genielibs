from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cat9k.c9610.configure import configure_hw_module_switch_slot_shutdown
from unittest.mock import Mock


class TestConfigureHwModuleSwitchSlotShutdown(TestCase):

    def test_configure_hw_module_switch_slot_shutdown(self):
        self.device = Mock()
        result = configure_hw_module_switch_slot_shutdown(self.device, 1, 1, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('hw-module switch 1 slot 1 shutdown',)
        )
    def test_configure_hw_module_switch_subslot_shutdown(self):
        self.device = Mock()
        result = configure_hw_module_switch_slot_shutdown(self.device, 1, None, 1)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('hw-module switch 1 subslot 1 shutdown',)
        )
