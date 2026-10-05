import unittest
from unittest.mock import Mock

from genie.conf.base.device import Device
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.execute import (
    execute_set_config_register,
)
from genie.libs.sdk.apis.iosxe.cat9k.platform.execute import (
    execute_set_config_register as cat9k_execute_set_config_register,
)


class TestExecuteSetConfigRegister(unittest.TestCase):

    def test_execute_set_config_register_enable_mode(self):
        device = Mock()
        device.name = 'c9800'
        device.subconnections = None
        device.default.state_machine.current_state = 'enable'
        device.default.role = 'active'

        execute_set_config_register(device, '0x2102')

        device.default.configure.assert_called_once_with(
            'config-register 0x2102', timeout=300
        )

    def test_execute_set_config_register_rommon_mode(self):
        device = Mock()
        device.name = 'c9800'
        device.subconnections = None
        device.default.state_machine.current_state = 'rommon'
        device.default.role = 'active'

        execute_set_config_register(device, '0x2102')

        device.default.execute.assert_called_once_with(
            'confreg 0x2102', timeout=300
        )

    def test_dispatched_api_preserves_console_speed_bits(self):
        dispatch_device = Device(
            'uut', os='iosxe', platform='cat9k', model='c9800'
        )
        resolved_api = dispatch_device.api.get_api(
            'execute_set_config_register', dispatch_device
        )

        device = Mock()
        device.name = 'c9800'
        device.subconnections = None
        device.default.state_machine.current_state = 'rommon'
        device.default.role = 'active'
        device.api.get_config_register.return_value = '0x1922'

        resolved_api(
            device,
            '0x0',
            preserve_console_speed=True,
        )

        device.default.execute.assert_called_once_with(
            'confreg 0x1820', timeout=300
        )
        device.api.get_config_register.assert_called_once_with(
            device=device.default)

    def test_execute_set_config_register_skips_standby(self):
        device = Mock()
        device.name = 'c9800'
        device.subconnections = None
        device.default.state_machine.current_state = 'enable'
        device.default.role = 'standby'

        execute_set_config_register(device, '0x2102')

        device.default.configure.assert_not_called()

    def test_c9800_and_c9800_cl_resolve_to_c9800_api(self):
        platform_tokens = (
            {'platform': 'cat9k', 'model': 'c9800'},
            {
                'platform': 'cat9k',
                'model': 'c9800',
                'submodel': 'c9800_cl',
            },
        )

        for tokens in platform_tokens:
            with self.subTest(tokens=tokens):
                device = Device('uut', os='iosxe', **tokens)
                resolved_api = device.api.get_api(
                    'execute_set_config_register', device
                )
                self.assertIs(resolved_api, execute_set_config_register)

    def test_physical_cat9k_platforms_keep_cat9k_api(self):
        for model in ('c9300', 'c9400', 'c9500'):
            with self.subTest(model=model):
                device = Device(
                    model,
                    os='iosxe',
                    platform='cat9k',
                    model=model,
                )
                resolved_api = device.api.get_api(
                    'execute_set_config_register', device
                )
                self.assertIs(
                    resolved_api,
                    cat9k_execute_set_config_register,
                )
