import logging
import unittest
from types import SimpleNamespace

from unittest.mock import Mock, patch

from genie.libs.clean.stages.stages import PingServer
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Skipped
from pyats.aetest.signals import TerminateStepSignal
from unicon.core.errors import SubCommandFailure


# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Pingserver(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = PingServer()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()        
        data = '''
            Success rate is 80 percent (4/5)
            5 packets transmitted, 5 packets received, 0.00% packet loss
        '''
        
        # And we want the ping method to be mocked
        # To simulate pass case
        self.device.ping = Mock(return_value=data)

        # Call the method to be tested (clean step inside class)
        self.cls.ping_server(
            steps=steps, device=self.device, server='server-1'
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_fail_to_ping(self):
       # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the ping method to be mocked
        # To simulate fail case
        self.device.ping = Mock(side_effect=SubCommandFailure)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.ping_server(
                steps=steps, device=self.device, server='server-1', timeout=2, 
                interval=1, max_attempts=1
             )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


    def test_fail_minimum_success_rate(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data = '''
            Success rate is 80 percent (4/5)
            5 packets transmitted, 3 packets received, 0.00% packet loss
        '''
        
        # And we want the ping method to be mocked
        self.device.ping = Mock(return_value=data)

        # Call the method to be tested (clean step inside class)
        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.ping_server(
                steps=steps, device=self.device, server='server-1', timeout=2,
                min_success_rate=100, interval=1, 
                max_attempts=1
            )

        # Check that the result is expected
        self.assertEqual(Failed, steps.details[0].result)

    @patch('genie.libs.clean.stages.stages.time.sleep')
    def test_collects_before_retry_and_only_after_first_failure(self, sleep):
        steps = Steps()
        events = []
        self.device.ping = Mock(side_effect=[
            SubCommandFailure('ping failed'),
            'Success rate is 0 percent (0/5)',
            'Success rate is 100 percent (5/5)',
        ])
        self.device.execute = Mock(side_effect=lambda command: events.append(command))
        sleep.side_effect = lambda interval: events.append('retry')

        self.cls.ping_server(
            steps=steps, device=self.device, server='192.0.2.2',
            vrf='management', max_attempts=3, interval=1,
            diagnostics={'interface': 'GigabitEthernet1'},
        )

        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual([
            'show clock detail', 'show ip arp',
            'show interfaces GigabitEthernet1',
            'show ip interface GigabitEthernet1',
            'show running-config interface GigabitEthernet1',
            'show ip route vrf management 192.0.2.2',
            'retry', 'retry',
        ], events)

    def test_collects_both_endpoints_and_continues_after_diagnostic_error(self):
        linux = Mock(name='vm-1')
        linux.name = 'vm-1'
        linux.execute = Mock(return_value='output')
        linux.interfaces = {'fpnl': SimpleNamespace(name='eth0')}
        device = Mock(name='PE1')
        device.name = 'PE1'
        device.os = 'iosxe'
        device.interfaces = {'fpnl': SimpleNamespace(
            name='GigabitEthernet1',
            ipv4=SimpleNamespace(ip='192.0.2.1'),
        )}
        device.testbed.devices = {'vm-1': linux}
        device.execute = Mock(side_effect=[RuntimeError('command failed'),
                                           'output', 'output', 'output',
                                           'output', 'output'])

        self.cls._collect_connectivity_diagnostics(
            device, '192.0.2.2', 'management', {
                'interface': 'fpnl',
                'linux_device': 'vm-1',
                'linux_interface': 'fpnl',
            },
        )

        self.assertEqual([
            'show clock detail', 'show ip arp',
            'show interfaces GigabitEthernet1',
            'show ip interface GigabitEthernet1',
            'show running-config interface GigabitEthernet1',
            'show ip route vrf management 192.0.2.2',
        ], [call.args[0] for call in device.execute.call_args_list])
        self.assertEqual([
            'date -u', 'ip -br address', 'ip -s link show dev eth0',
            'ip route get 192.0.2.1', 'ip neigh show dev eth0',
        ], [call.args[0] for call in linux.execute.call_args_list])

    def test_success_does_not_collect_diagnostics(self):
        steps = Steps()
        self.device.ping = Mock(return_value='Success rate is 100 percent (5/5)')
        self.device.execute = Mock()

        self.cls.ping_server(
            steps=steps, device=self.device, server='192.0.2.2',
            diagnostics={'interface': 'GigabitEthernet1'},
        )

        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_not_called()

    @patch('genie.libs.clean.stages.stages.time.sleep')
    @patch('genie.libs.sdk.apis.utils.collect_ping_failure_diagnostics')
    def test_below_threshold_calls_sdk_before_retry(self, collect, sleep):
        steps = Steps()
        events = []
        self.device.ping = Mock(side_effect=[
            'Success rate is 20 percent (1/5)',
            'Success rate is 100 percent (5/5)',
        ])
        collect.side_effect = lambda *args, **kwargs: events.append('collect')
        sleep.side_effect = lambda interval: events.append('retry')

        self.cls.ping_server(
            steps=steps, device=self.device, server='192.0.2.2',
            max_attempts=2, diagnostics={'interface': 'fpnl'})

        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(['collect', 'retry'], events)
        collect.assert_called_once_with(
            self.device, '192.0.2.2', vrf=None, interface='fpnl')

