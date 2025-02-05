import os
import unittest
from unittest import mock
from genie.libs.sdk.apis.iosxe.cat9k.rommon.utils import send_break_boot
        
class TestSendBreakBoot(unittest.TestCase):
    @mock.patch('genie.libs.sdk.apis.iosxe.cat9k.rommon.utils.xe_generic_break_boot')
    def test_send_break_boot(self, mock_generic_break_boot):
        # Create a mock device object
        mock_device = mock.Mock()
        
        # Call the send_break_boot function
        send_break_boot(mock_device)
        
        # Verify that generic_break_boot was called with the correct arguments
        mock_generic_break_boot.assert_called_once_with(
            mock_device,
            console_activity_pattern=r'\[.*Ctrl-C.*\]',
            console_breakboot_char='\x03',
            console_breakboot_telnet_break=None,
            grub_activity_pattern=None,
            grub_breakboot_char=None,
            break_count=2,
            timeout=60
        )