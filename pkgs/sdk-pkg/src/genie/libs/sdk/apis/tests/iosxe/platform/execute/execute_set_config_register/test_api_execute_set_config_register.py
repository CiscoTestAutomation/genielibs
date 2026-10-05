from unittest import TestCase
from unittest.mock import Mock, call

from genie.libs.sdk.apis.iosxe.platform.execute import (
    execute_set_config_register,
)


class TestExecuteSetConfigRegister(TestCase):

    def _make_device(self, *, current_confreg='0x2102', state='rommon'):
        device = Mock()
        device.name = 'router'
        device.default = Mock()
        device.default.state_machine = Mock()
        device.default.state_machine.current_state = state
        device.default.role = 'active'
        device.subconnections = [device.default]
        device.api.get_config_register.return_value = current_confreg
        return device

    def test_recovery_request_does_not_depend_on_terminal_server_metadata(self):
        device = self._make_device(current_confreg='0x1922')
        device.peripherals = {}
        execute_set_config_register(
            device, config_register='0x0', preserve_console_speed=True)
        args, _ = device.default.execute.call_args
        self.assertEqual(args[0], f'confreg {hex(0x1922 & 0x1820)}')
        device.api.get_config_register.assert_called_once_with(
            device=device.default)

    def test_preserves_console_speed_bits_per_subconnection(self):
        active = Mock()
        active.state_machine.current_state = 'rommon'
        active.role = 'active'
        standby = Mock()
        standby.state_machine.current_state = 'rommon'
        standby.role = 'standby'

        device = Mock()
        device.name = 'router'
        device.subconnections = [active, standby]
        device.api.get_config_register.side_effect = ['0x1922', '0x1022']

        execute_set_config_register(
            device, config_register='0x0', preserve_console_speed=True)

        active.execute.assert_called_once_with(
            'confreg 0x1820', timeout=300)
        standby.execute.assert_called_once_with(
            'confreg 0x1020', timeout=300)
        device.api.get_config_register.assert_has_calls([
            call(device=active),
            call(device=standby),
        ])
        self.assertEqual(device.api.get_config_register.call_count, 2)

    def test_default_writes_requested_zero(self):
        device = self._make_device(current_confreg='0x1922')
        execute_set_config_register(device, config_register='0x0')
        args, _ = device.default.execute.call_args
        self.assertEqual(args[0], 'confreg 0x0')
        device.api.get_config_register.assert_not_called()

    def test_non_zero_requested_value_passes_through(self):
        device = self._make_device(current_confreg='0x1922')
        execute_set_config_register(
            device, config_register='0x2102', preserve_console_speed=True)
        args, _ = device.default.execute.call_args
        self.assertEqual(args[0], 'confreg 0x2102')
        device.api.get_config_register.assert_not_called()

    def test_preservation_request_outside_rommon_writes_exact_value(self):
        device = self._make_device(current_confreg='0x1922', state='enable')
        execute_set_config_register(
            device, config_register='0x0', preserve_console_speed=True)
        device.default.configure.assert_called_once_with(
            'config-register 0x0', timeout=300)
        device.api.get_config_register.assert_not_called()

    def test_unreadable_current_register_falls_back_to_requested(self):
        device = self._make_device(current_confreg=None)
        execute_set_config_register(
            device, config_register='0x0', preserve_console_speed=True)
        args, _ = device.default.execute.call_args
        self.assertEqual(args[0], 'confreg 0x0')
