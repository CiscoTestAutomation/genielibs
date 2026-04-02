from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.platform.execute import execute_set_config_register
from unittest.mock import Mock


class TestExecuteSetConfigRegister(TestCase):
    def test_execute_set_config_register(self):
        device = Mock()
        device.execute = Mock()
        device.configure = Mock()

        device.state_machine.current_state = 'rommon'
        execute_set_config_register(device, config_register='0x2102')
        device.execute.assert_called_once_with('set var ConfigReg=0x2102', timeout=300)

        device.state_machine.current_state = 'enable'
        execute_set_config_register(device, config_register='0x2102')
        device.configure.assert_called_once_with('config-register 0x2102', timeout=300)
