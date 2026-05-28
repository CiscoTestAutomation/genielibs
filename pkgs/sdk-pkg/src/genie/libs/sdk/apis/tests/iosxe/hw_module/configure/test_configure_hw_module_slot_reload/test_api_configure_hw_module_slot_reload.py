from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.hw_module.configure import configure_hw_module_slot_reload


class TestConfigureHwModuleSlotReload(TestCase):

    def test_configure_hw_module_slot_reload(self):
        self.device = Mock()
        configure_hw_module_slot_reload(self.device, slot=3)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('hw-module slot 3 reload',)
        )
