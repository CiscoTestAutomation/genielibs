from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_monitor_session
from unittest.mock import Mock


class TestConfigureInterfaceMonitorSession(TestCase):

    def test_configure_interface_monitor_session(self):
        self.device = Mock()
        result = configure_interface_monitor_session(self.device, [{'erspan_id': 101,
  'interface': 'FiftyGigE1/0/4',
  'ipv6_address': '2040::1',
  'monitor_direction': 'rx',
  'session_name': 6,
  'session_type': 'erspan-source'},
 {'erspan_id': 102,
  'interface': 'FiftyGigE1/0/4',
  'ip_address': '192.168.0.2',
  'monitor_direction': 'rx',
  'session_name': 4,
  'session_type': 'erspan-source'}])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (('monitor session 6 type erspan-source\n'
 'source interface FiftyGigE1/0/4 rx\n'
 'destination\n'
 'erspan-id 101\n'
 'ipv6 address 2040::1\n'
 'exit\n'
 'no shutdown\n'),)
        )
        self.assertEqual(
            self.device.configure.mock_calls[1].args,
            (('monitor session 4 type erspan-source\n'
 'source interface FiftyGigE1/0/4 rx\n'
 'destination\n'
 'erspan-id 102\n'
 'ip address 192.168.0.2\n'
 'exit\n'
 'no shutdown\n'),)
        )
