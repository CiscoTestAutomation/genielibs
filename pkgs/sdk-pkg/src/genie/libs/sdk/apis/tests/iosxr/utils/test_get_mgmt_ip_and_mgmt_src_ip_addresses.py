import unittest
from textwrap import dedent
from unittest.mock import Mock, call

from genie.conf.base.device import Device
from genie.libs.sdk.apis.iosxr.spitfire.utils import get_mgmt_ip_and_mgmt_src_ip_addresses


class testAPI(unittest.TestCase):

    def test_get_mgmt_ip_and_mgmt_src_ip_addresses(self):
        device = Device(
            name='Router',
            os='iosxr',
            platform='spitfire',
            custom=dict(abstraction=dict(order=['os', 'platform']))
        )
        device.is_connected = Mock(return_value=True)
        device.execute = Mock(return_value=dedent('''
        Active Internet connections (servers and established)
        Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
        tcp        0      0 0.0.0.0:179             0.0.0.0:*               LISTEN      1131/bgp        
        tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      7756/sshd       
        tcp        0      0 0.0.0.0:830             0.0.0.0:*               LISTEN      7756/sshd       
        tcp        0    188 1.1.1.95:22             2.2.2.145:50173         ESTABLISHED 12021/sshd: admin [
        tcp6       0      0 :::179                  :::*                    LISTEN      1131/bgp        
        tcp6       0      0 :::22                   :::*                    LISTEN      7756/sshd       
        tcp6       0      0 :::830                  :::*                    LISTEN      7756/sshd       
        '''))

        with self.assertLogs('genie.libs.sdk.apis.iosxr.spitfire.utils') as cm:
            result = get_mgmt_ip_and_mgmt_src_ip_addresses(device)
            self.assertEqual(cm.output,[
                "INFO:genie.libs.sdk.apis.iosxr.spitfire.utils:Device management IP: 1.1.1.95",
                "INFO:genie.libs.sdk.apis.iosxr.spitfire.utils:Device management source IP addresses: {'2.2.2.145'}"
            ])
            self.assertEqual(result, ('1.1.1.95', {'2.2.2.145'}))

        device.execute.assert_has_calls([call('bash netstat -antp')])

    def test_get_mgmt_ip_and_mgmt_src_ip_addresses1(self):
        device = Device(
            name='Router',
            os='iosxr',
            platform='spitfire',
            custom=dict(abstraction=dict(order=['os', 'platform']))
        )
        device.is_connected = Mock(return_value=True)
        device.execute = Mock(return_value=dedent('''
        Active Internet connections (servers and established)
        Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
        tcp        0      0 0.0.0.0:179             0.0.0.0:*               LISTEN      1131/bgp        
        tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      7756/sshd       
        tcp        0      0 0.0.0.0:830             0.0.0.0:*               LISTEN      7756/sshd       
        tcp        0    188 1.1.1.95:22             2.2.2.145:50173         ESTABLISHED 12021/sshd: admin [
        tcp6       0      0 :::179                  :::*                    LISTEN      1131/bgp        
        tcp6       0      0 :::22                   :::*                    LISTEN      7756/sshd       
        tcp6       0      0 :::830                  :::*                    LISTEN      7756/sshd       
        '''))

        with self.assertLogs('genie.libs.sdk.apis.iosxr.spitfire.utils') as cm:
            result = get_mgmt_ip_and_mgmt_src_ip_addresses(device, mgmt_src_ip='2.2.2.145')
            self.assertEqual(cm.output,[
                "INFO:genie.libs.sdk.apis.iosxr.spitfire.utils:Device management IP: 1.1.1.95",
                "INFO:genie.libs.sdk.apis.iosxr.spitfire.utils:Device management source IP addresses: {'2.2.2.145'}"
            ])
            self.assertEqual(result, ('1.1.1.95', {'2.2.2.145'}))

        device.execute.assert_has_calls([call('bash netstat -antp')])