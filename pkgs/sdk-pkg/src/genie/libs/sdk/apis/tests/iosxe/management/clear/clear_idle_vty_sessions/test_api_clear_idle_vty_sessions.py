from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.clear import clear_idle_vty_sessions
from unittest.mock import Mock, patch

class TestClearIdleVtySessions(TestCase):

    @patch('genie.libs.sdk.apis.iosxe.management.clear.log')
    def test_clear_idle_vty_sessions(self, mocked_log):
        self.device = Mock()
        self.device.parse = Mock(return_value={'line': {\
                           '867 vty 1': {'host': 'idle', 'idle': '10:20:30', 'location': \
                           '172.21.179.28', 'active': True}}})

        clear_idle_vty_sessions(self.device)
        mocked_log.info.assert_called_with("No idle sessions, not clearing vty sessions")

    @patch('genie.libs.sdk.apis.iosxe.management.clear.log')
    def test_cannot_find_idle_timeout(self, mocked_log):
        self.device = Mock()
        self.device.parse = Mock(return_value={'line': {\
                           '867 vty 1': {'host': 'idle', 'location': \
                           '172.21.179.28', 'active': False}}})
        clear_idle_vty_sessions(self.device)
        mocked_log.warning.assert_called_with("Cannot find the idle timeout, not clearing vty sessions")

    @patch('genie.libs.sdk.apis.iosxe.management.clear.log')
    def test_cannot_find_idle_timeout_tty(self, mocked_log):
        self.device = Mock()
        self.device.parse = Mock(return_value={'line': {\
                           '867 tty 1': {'host': 'idle', 'location': \
                           '172.21.179.28', 'active': False}}})
        clear_idle_vty_sessions(self.device)
        mocked_log.info.assert_called_with("No idle sessions, not clearing vty sessions")

    def test_clear_idle_vty_sessions_with_hms(self):
        self.device = Mock()
        self.device.parse = Mock(return_value={'line': {\
                           '867 vty 1': {'host': 'idle', 'idle': '10:20:30', 'location': \
                           '172.21.179.28', 'active': False}}})

        clear_idle_vty_sessions(self.device)
        self.device.execute.assert_called_once_with('clear line 867')

    def test_clear_idle_vty_sessions_with_hm(self):
        self.device = Mock()
        self.device.parse = Mock(return_value={'line': {\
                           '867 vty 1': {'host': 'idle', 'idle': '10:20', 'location': \
                           '172.21.179.28', 'active': False}}})

        clear_idle_vty_sessions(self.device)
        self.device.execute.assert_called_once_with('clear line 867')

    def test_clear_idle_vty_sessions_with_dh(self):
        self.device = Mock()
        self.device.parse = Mock(return_value={'line': {\
                           '867 vty 1': {'host': 'idle', 'idle': '6d14h', 'location': \
                           '172.21.179.28', 'active': False}}})

        clear_idle_vty_sessions(self.device)
        self.device.execute.assert_called_once_with('clear line 867')

    def test_clear_idle_vty_sessions_with_dh_1(self):
        self.device = Mock()
        self.device.parse = Mock(return_value={
            'line': {
                '1 tty 1': {
                    'active': False,
                    'host': 'incoming',
                    'idle': '1d23h',
                    'location': '10.85.191.9',
                },
                '18 vty 0': {
                    'active': False,
                    'host': 'idle',
                    'idle': '6d18h',
                    'location': '172.21.179.28',
                },
                '19 vty 1': {
                    'active': True,
                    'host': 'idle',
                    'idle': '00:00:00',
                    'location': '10.61.200.146',
                },
                }
        })
        clear_idle_vty_sessions(self.device)
        self.device.execute.assert_called_once_with('clear line 18')