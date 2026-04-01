from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ie3k.platform.get import get_config_register


class TestGetConfigRegister(TestCase):
    @classmethod
    def setUpClass(self):
        self.device = Mock()
        self.device.execute = Mock()

    def test_get_config_register_cli(self):
        expected_result = '0x2102'
        self.device.state_machine.current_state = 'enable'
        self.device.execute.return_value = '''
            BAUD = 115200
            BL_UPGRADE_RESET = no
            APPLY_RESET = no
            RET_2_RTS =
            FIPS_MODE =
            CSDL_MODE_DISABLE =
            CSDL_ENTROPY_REQUIREMENT_DISABLE =
            MANUAL_BOOT = yes
            ConfigReg = 0x2102
            BSI = 0
        '''
        actual_result = get_config_register(self.device)
        self.device.execute.assert_called_with('show romvar')
        self.assertEqual(actual_result, expected_result)

    def test_get_config_register_rommon(self):
        expected_result = '0x0'
        self.device.state_machine.current_state = 'rommon'
        self.device.execute.return_value = '''
            APPLY_RESET=no
            BAUD=115200
            BL_UPGRADE_RESET=no
            BSI=0
            CSDL_ENTROPY_REQUIREMENT_DISABLE=
            CSDL_MODE_DISABLE=
            ConfigReg=0x0
            FIPS_MODE=
            MANUAL_BOOT=yes
            RET_2_RTS=
        '''
        actual_result = get_config_register(self.device)
        self.device.execute.assert_called_with('set')
        self.assertEqual(actual_result, expected_result)
