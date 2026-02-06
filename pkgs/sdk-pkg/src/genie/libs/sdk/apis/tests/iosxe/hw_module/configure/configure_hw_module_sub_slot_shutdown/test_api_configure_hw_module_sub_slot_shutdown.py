from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hw_module.configure import configure_hw_module_sub_slot_shutdown
from unittest.mock import Mock


class TestConfigureHwModuleSubSlotShutdown(TestCase):

    def test_configure_hw_module_sub_slot_shutdown(self):
        self.device = Mock()
        result = configure_hw_module_sub_slot_shutdown(self.device, '0/1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('hw-module subslot 0/1 shutdown unpowered',)
        )
