import unittest
from unittest.mock import Mock

from genie.conf.base.device import Device
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.configure import (
    configure_no_boot_manual,
)
from genie.libs.sdk.apis.iosxe.platform.configure import configure_autoboot


class TestConfigureNoBootManual(unittest.TestCase):

    def test_configure_no_boot_manual_sets_autoboot_register(self):
        device = Mock()
        device.api.configure_autoboot.side_effect = (
            lambda: configure_autoboot(device)
        )

        configure_no_boot_manual(device)

        device.api.configure_autoboot.assert_called_once_with()
        device.api.execute_set_config_register.assert_called_once_with(
            config_register='0x2102'
        )

    def test_configure_no_boot_manual_propagates_failure(self):
        device = Mock()
        error = RuntimeError('Unable to configure autoboot')
        device.api.configure_autoboot.side_effect = error

        with self.assertRaises(RuntimeError) as raised:
            configure_no_boot_manual(device)

        self.assertIs(raised.exception, error)

    def test_c9800_and_c9800_cl_resolve_to_platform_implementation(self):
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
                    'configure_no_boot_manual', device
                )

                self.assertIs(resolved_api, configure_no_boot_manual)
