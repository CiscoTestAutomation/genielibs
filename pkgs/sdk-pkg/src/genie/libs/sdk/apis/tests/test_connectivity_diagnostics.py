"""Tests for ping failure diagnostics shared by scripts and Clean."""

import logging
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from genie.libs.sdk.apis.utils import (
    collect_ping_failure_diagnostics)


class TestCollectPingFailureDiagnostics(unittest.TestCase):

    def setUp(self):
        self._logging_disabled = logging.root.manager.disable
        logging.disable(logging.NOTSET)
        self.device = SimpleNamespace(
            name='uut',
            interfaces={'fpnl': SimpleNamespace(
                name='GigabitEthernet1',
                ipv4=SimpleNamespace(ip='192.0.2.1'))},
            execute=Mock(return_value='captured'),
        )
        self.linux = SimpleNamespace(
            name='vm', alias='jumphost',
            interfaces={'fpnl': SimpleNamespace(name='ens34')},
            execute=Mock(return_value='captured'),
        )
        self.device.testbed = SimpleNamespace(devices={'vm': self.linux})

    def tearDown(self):
        logging.disable(self._logging_disabled)

    def test_collects_both_endpoints_using_testbed_aliases(self):
        result = collect_ping_failure_diagnostics(
            self.device, '192.0.2.2', vrf='management', interface='fpnl',
            linux_device='jumphost', linux_interface='fpnl')

        self.assertEqual([
            'show clock detail', 'show ip arp',
            'show interfaces GigabitEthernet1',
            'show ip interface GigabitEthernet1',
            'show running-config interface GigabitEthernet1',
            'show ip route vrf management 192.0.2.2',
        ], [call.args[0] for call in self.device.execute.call_args_list])
        self.assertEqual([
            'date -u', 'ip -br address', 'ip -s link show dev ens34',
            'ip route get 192.0.2.1', 'ip neigh show dev ens34',
        ], [call.args[0] for call in self.linux.execute.call_args_list])
        self.assertEqual('captured', result['cisco']['show clock detail'])
        self.assertEqual('captured', result['linux']['date -u'])

    def test_failed_command_does_not_stop_collection(self):
        self.device.execute.side_effect = [RuntimeError('unavailable')] + [
            'captured'] * 5

        with self.assertLogs(
                'genie.libs.sdk.apis.utils', 'WARNING'):
            result = collect_ping_failure_diagnostics(
                self.device, '192.0.2.2', interface='fpnl')

        self.assertIsNone(result['cisco']['show clock detail'])
        self.assertEqual('captured', result['cisco']['show ip arp'])
        self.assertEqual(6, self.device.execute.call_count)

    def test_invalid_destination_still_collects_other_commands(self):
        with self.assertLogs(
                'genie.libs.sdk.apis.utils', 'WARNING'):
            result = collect_ping_failure_diagnostics(
                self.device, 'unresolved-host')

        self.assertEqual(['show clock detail', 'show ip arp'],
                         list(result['cisco']))


if __name__ == '__main__':
    unittest.main()
