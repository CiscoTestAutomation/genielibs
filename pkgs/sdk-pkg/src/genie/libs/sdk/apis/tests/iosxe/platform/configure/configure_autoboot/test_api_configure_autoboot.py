import unittest
from unittest.mock import Mock

from genie.conf.base.device import Device
from genie.libs.sdk.apis.iosxe.platform.configure import configure_autoboot
from unicon.core.errors import SubCommandFailure


class TestConfigureAutoboot(unittest.TestCase):

    def test_configure_autoboot(self):
        device = Mock()
        configure_autoboot(device)
        device.api.execute_set_config_register.assert_called_once_with(
            config_register='0x2102'
        )

    def test_configure_autoboot_failure(self):
        device = Mock()
        error = Exception('Unable to set config-register')
        device.api.execute_set_config_register.side_effect = error

        with self.assertRaises(SubCommandFailure) as raised:
            configure_autoboot(device)

        self.assertIn('Could not configure autoboot', str(raised.exception))

    def test_platforms_resolve_to_generic_implementation(self):
        platform_tokens = (
            ('c1k', {'platform': 'c1k'}),
            ('asr1k', {'platform': 'asr1k'}),
            ('c8kv', {'platform': 'c8kv'}),
            ('cat8k', {'platform': 'cat8k'}),
            ('cat9kv', {'platform': 'cat9kv'}),
            ('c9400', {'platform': 'cat9k', 'model': 'c9400'}),
            ('c9800', {'platform': 'cat9k', 'model': 'c9800'}),
            ('c9800_cl', {
                'platform': 'cat9k',
                'model': 'c9800',
                'submodel': 'c9800_cl',
            }),
            ('isr4k', {'platform': 'isr4k'}),
        )

        for name, tokens in platform_tokens:
            with self.subTest(platform=name):
                device = Device(name=name, os='iosxe', **tokens)
                resolved_api = device.api.get_api(
                    'configure_autoboot', device
                )
                self.assertIs(resolved_api, configure_autoboot)
