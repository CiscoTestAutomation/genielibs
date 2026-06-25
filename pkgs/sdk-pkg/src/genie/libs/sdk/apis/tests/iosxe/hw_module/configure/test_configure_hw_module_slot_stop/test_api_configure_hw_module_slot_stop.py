from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.hw_module.configure import configure_hw_module_slot_stop


class TestConfigureHwModuleSlotStop(TestCase):

    def test_configure_hw_module_slot_stop(self):
        self.device = Mock()
        test_slot = 1

        configure_hw_module_slot_stop(self.device, slot=test_slot)

        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('hw-module slot 1 stop',)
        )
