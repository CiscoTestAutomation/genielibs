import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_hw_module_slot_upoe_plus


class TestUnconfigureHwModuleSlotUpoePlus(unittest.TestCase):

    def test_unconfigure_hw_module_slot_upoe_plus(self):
        device = Mock()

        result = unconfigure_hw_module_slot_upoe_plus(device, 2)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no hw-module slot 2 upoe-plus',)
        )