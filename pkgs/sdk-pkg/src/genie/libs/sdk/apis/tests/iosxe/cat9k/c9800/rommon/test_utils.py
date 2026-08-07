import unittest
from unittest import mock
from genie.libs.sdk.apis.iosxe.cat9k.c9800.rommon.utils import send_break_boot


class TestC9800SendBreakBoot(unittest.TestCase):
    @mock.patch('genie.libs.sdk.apis.iosxe.cat9k.c9800.rommon.utils.cat9k_break_boot')
    def test_send_break_boot_grub_defaults(self, mock_cat9k_break_boot):
        """C9800 send_break_boot should set GRUB defaults for vWLC."""
        mock_device = mock.Mock()

        send_break_boot(mock_device)

        mock_cat9k_break_boot.assert_called_once_with(
            mock_device,
            console_activity_pattern=None,
            console_breakboot_char=None,
            console_breakboot_telnet_break=None,
            grub_activity_pattern='The highlighted entry will be (?:booted|executed) automatically',
            grub_breakboot_char='c',
            break_count=2,
            timeout=60
        )

    @mock.patch('genie.libs.sdk.apis.iosxe.cat9k.c9800.rommon.utils.cat9k_break_boot')
    def test_send_break_boot_caller_overrides(self, mock_cat9k_break_boot):
        """Caller-provided values should override GRUB defaults."""
        mock_device = mock.Mock()

        send_break_boot(mock_device,
                        grub_activity_pattern='custom pattern',
                        grub_breakboot_char='e',
                        console_activity_pattern='custom console',
                        timeout=120)

        mock_cat9k_break_boot.assert_called_once_with(
            mock_device,
            console_activity_pattern='custom console',
            console_breakboot_char=None,
            console_breakboot_telnet_break=None,
            grub_activity_pattern='custom pattern',
            grub_breakboot_char='e',
            break_count=2,
            timeout=120
        )


if __name__ == '__main__':
    unittest.main()
