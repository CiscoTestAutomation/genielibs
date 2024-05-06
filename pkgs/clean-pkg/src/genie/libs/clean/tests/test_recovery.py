import unittest
from unittest.mock import Mock, MagicMock, patch

from unicon import Connection
from unicon.settings import Settings

from genie.libs.clean.recovery.recovery import recovery_processor

import logging

logger = logging.getLogger(__name__)


class MockDisconnectReconnect:

    def __init__(self, *args, **kwargs):
        self.state = iter([False, True, False, True])

    def __call__(self, *arg, **kwargs):
        state = next(self.state)
        return state


mock_disconnect_reconnect =  MockDisconnectReconnect()



class TestRecovery(unittest.TestCase):

    def test_recovery_processor_device_in_rommon(self):

        section = Mock()
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.is_ha = False
        device.state_machine.go_to = MagicMock()
        device.state_machine.current_state = 'rommon'
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.log = logger

        recovery_processor(
            section,
            console_activity_pattern='Initializing Hardware',
            console_breakboot_telnet_break=True,
            break_count=1,
            golden_image=['bootflash:asr1000_golden.bin'],
            reconnect_delay=1)
        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_power_cycle_device.assert_not_called()

    def test_recovery_processor_device_in_rommon_ha(self):
        section = Mock()
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.is_ha = True
        sub_con_1 = sub_con_2 = MagicMock()
        sub_con_1.state_machine.current_state = sub_con_2.state_machine.current_state = 'rommon'
        device.subconnections = [sub_con_1, sub_con_2]
        device.api.device_boot_recovery = Mock()
        device.api.execute_power_cycle_device = Mock()
        recovery_processor(
            section,
            console_activity_pattern='Initializing Hardware',
            console_breakboot_telnet_break=True,
            break_count=1,
            golden_image=['bootflash:asr1000_golden.bin'],
            reconnect_delay=1)
        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_power_cycle_device.assert_not_called()

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect', new=mock_disconnect_reconnect)
    def test_recovery_processor_recovery_failed(self):
        section = Mock()
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.state_machine.go_to = Mock(side_effect=Exception)
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_console = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.is_ha = False
        device.log = logger
        recovery_processor(
            section,
            console_activity_pattern='Initializing Hardware',
            console_breakboot_telnet_break=True,
            break_count=1,
            golden_image=['bootflash:asr1000_golden.bin'],
            reconnect_delay=1)
        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_clear_console.assert_called_once()
        device.api.execute_power_cycle_device.assert_called_once()
        self.assertTrue(section.parent.parameters['block_section'])

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect', new=mock_disconnect_reconnect)
    def test_recovery_processor_recovery_failed_ha(self):
        section = Mock()
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.state_machine.go_to = Mock(side_effect=Exception)
        device.os = 'iosxe'
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_console = Mock()
        device.api.execute_power_cycle_device = Mock()
        device.log = logger
        device.is_ha = True
        device.api.device_boot_recovery = Mock()
        device.api.execute_clear_console = Mock()
        sub_con_1 = sub_con_2 = MagicMock()
        sub_con_1.state_machine.go_to = Mock(side_effect=Exception)
        device.subconnections = [sub_con_1, sub_con_2]
        recovery_processor(
            section,
            console_activity_pattern='Initializing Hardware',
            console_breakboot_telnet_break=True,
            break_count=1,
            golden_image=['bootflash:asr1000_golden.bin'],
            reconnect_delay=1)
        device.api.device_recovery_boot.assert_called_once()
        device.api.execute_clear_console.assert_called_once()
        device.api.execute_power_cycle_device.assert_called_once()
        self.assertTrue(section.parent.parameters['block_section'])