from unittest import TestCase
from unittest.mock import Mock, MagicMock

from genie.libs.sdk.apis.iosxe.utils import btdecode_grep


class TestBtdecodeGrep(TestCase):

    def test_btdecode_grep(self):
        self.device = Mock()
      

        # device.execute is only used for SELinux commands now
        selinux_map = {
            'set platform software selinux permissive': '',
            'set platform software selinux default': '',
        }

        def execute_side_effect(arg, **kwargs):
            return selinux_map.get(arg, '')

        self.device.execute.side_effect = execute_side_effect

        # Mock device.bash_console() as a context manager that yields a bash handle
        bash = Mock()
        bash.execute.return_value = '''2026/05/08 07:50:37.813883128 {paed_R0-0}{1}: [pae_channel] [329]: UUID: 0, ra: 0 (ERR): Channel not configured, Polling timer has been canceled
2026/05/08 07:55:37.813570713 {paed_R0-0}{1}: [pae_channel] [329]: UUID: 0, ra: 0 (ERR): Channel not configured, Polling timer has been canceled
2026/05/08 08:16:35.632007249 {iosrp_R0-0}{1}: [feat-telem] [6472]: UUID: 0, ra: 0 (note): FT-BG-Process: timer expired. CleanSeen 1, PAE 1, FT 1, actv 1
2026/05/08 09:14:39.990579887 {install_mgr_R0-0}{1}: [install_mgr] [14247]: UUID: 0, ra: 0 (note): INSTALL_MGR location_info: get auto_abort_timer state chas/fru/slot/bay:1/0/0/0 active:0 end_time:0'''

        bash_cm = MagicMock()
        bash_cm.__enter__.return_value = bash
        bash_cm.__exit__.return_value = False
        self.device.bash_console.return_value = bash_cm

        # Call the API
        result = btdecode_grep(self.device, '/tmp/rp/trace/utf*', 'timer', 60)

        # 1. Verify SELinux was set to permissive, then reset to default
        self.device.execute.assert_any_call('set platform software selinux permissive')
        self.device.execute.assert_any_call('set platform software selinux default')

        # 2. Verify bash_console was entered and the btdecode|grep command was run
        self.device.bash_console.assert_called_once()
        bash.execute.assert_called_once_with(
            'btdecode /tmp/rp/trace/utf* | grep "timer"',
            timeout=60,
        )

        # 3. Verify the returned dict contains only timestamped lines
        self.assertIn('matched_lines', result)
        self.assertEqual(len(result['matched_lines']), 4)
        

