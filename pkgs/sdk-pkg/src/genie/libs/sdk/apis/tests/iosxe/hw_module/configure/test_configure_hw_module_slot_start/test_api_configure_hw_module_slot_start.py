from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.hw_module.configure import configure_hw_module_slot_start


class TestConfigureHwModuleSlotStart(TestCase):

    def test_configure_hw_module_slot_start(self):
        self.device = Mock()
        slot = 2
        configure_hw_module_slot_start(self.device, slot=slot)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('hw-module slot 2 start',)
        )
