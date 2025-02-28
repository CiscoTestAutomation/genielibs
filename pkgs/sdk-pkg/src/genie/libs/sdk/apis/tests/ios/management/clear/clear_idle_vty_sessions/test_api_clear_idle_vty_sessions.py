from unittest import TestCase
from genie.libs.sdk.apis.ios.management.clear import clear_idle_vty_sessions
from unittest.mock import Mock

class TestClearIdleVtySessions(TestCase):

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