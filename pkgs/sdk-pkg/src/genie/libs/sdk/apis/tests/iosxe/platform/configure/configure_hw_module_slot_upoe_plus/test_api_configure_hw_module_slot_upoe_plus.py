from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_hw_module_slot_upoe_plus


class TestConfigureHwModuleSlotUpoePlus(TestCase):

    def test_configure_hw_module_slot_upoe_plus(self):
        device = Mock()
        result = configure_hw_module_slot_upoe_plus(
            device,
            2
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('hw-module slot 2 upoe-plus',)
        )