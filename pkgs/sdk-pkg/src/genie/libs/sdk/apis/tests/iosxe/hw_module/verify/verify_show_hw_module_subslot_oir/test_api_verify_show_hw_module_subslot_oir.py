from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.hw_module.verify import (
    verify_show_hw_module_subslot_oir,
)


class TestVerifyShowHwModuleSubslotOir(TestCase):

    def test_verify_show_hw_module_subslot_oir(self):
        self.device = Mock()
        parsed = {
            'subslots': {
                '0/1': {
                    'model': 'C1127-ES-8',
                    'operational_status': 'ok',
                }
            }
        }
        self.device.api.get_hw_module_subslot_oir = Mock(
            return_value=parsed)
        result = verify_show_hw_module_subslot_oir(
            self.device, '0/1', 'ok', max_time=5, check_interval=1)
        self.assertEqual(result, True)
        self.device.api.get_hw_module_subslot_oir.\
            assert_called_with(subslot='0/1')

    def test_verify_show_hw_module_subslot_oir_mismatch(self):
        self.device = Mock()
        parsed = {
            'subslots': {
                '0/1': {
                    'model': 'C1127-ES-8',
                    'operational_status': 'booting',
                }
            }
        }
        self.device.api.get_hw_module_subslot_oir = Mock(
            return_value=parsed)
        result = verify_show_hw_module_subslot_oir(
            self.device, '0/1', 'ok', max_time=1, check_interval=1)
        self.assertEqual(result, False)

    def test_verify_show_hw_module_subslot_oir_none(self):
        self.device = Mock()
        self.device.api.get_hw_module_subslot_oir = Mock(
            return_value=None)
        result = verify_show_hw_module_subslot_oir(
            self.device, '0/1', 'ok', max_time=1, check_interval=1)
        self.assertEqual(result, False)
