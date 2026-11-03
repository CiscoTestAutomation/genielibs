import unittest
from unittest import mock

from genie.conf.base.device import Device
from genie.libs.sdk.apis.iosxe.cat8k.rommon.utils import send_break_boot


class TestSendBreakBoot(unittest.TestCase):

    def test_cat8k_resolves_to_platform_implementation(self):
        device = Device(
            name='c8500', os='iosxe', platform='cat8k', model='c8500'
        )

        resolved_api = device.api.get_api('send_break_boot', device)

        self.assertIs(resolved_api, send_break_boot)

    @mock.patch(
        'genie.libs.sdk.apis.iosxe.cat8k.rommon.utils.xe_generic_break_boot'
    )
    def test_cat8k_defaults(self, mock_generic_break_boot):
        device = mock.Mock()

        send_break_boot(device, break_count=50, timeout=420)

        mock_generic_break_boot.assert_called_once_with(
            device,
            console_activity_pattern=r'.*System Bootstrap, Version.*',
            console_breakboot_char=None,
            console_breakboot_telnet_break=True,
            grub_activity_pattern=None,
            grub_breakboot_char=None,
            break_count=50,
            timeout=420,
        )

    @mock.patch(
        'genie.libs.sdk.apis.iosxe.cat8k.rommon.utils.xe_generic_break_boot'
    )
    def test_cat8k_preserves_activity_pattern_and_uses_telnet_break(
            self, mock_generic_break_boot):
        device = mock.Mock()

        send_break_boot(
            device,
            console_activity_pattern='custom activity',
            console_breakboot_char='custom character',
            console_breakboot_telnet_break=False,
            grub_activity_pattern='grub activity',
            grub_breakboot_char='grub character',
            break_count=7,
            timeout=90,
        )

        mock_generic_break_boot.assert_called_once_with(
            device,
            console_activity_pattern='custom activity',
            console_breakboot_char='custom character',
            console_breakboot_telnet_break=True,
            grub_activity_pattern='grub activity',
            grub_breakboot_char='grub character',
            break_count=7,
            timeout=90,
        )
