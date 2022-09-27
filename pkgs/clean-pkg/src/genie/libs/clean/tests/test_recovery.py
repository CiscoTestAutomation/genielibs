import unittest
from unittest.mock import Mock, MagicMock, patch

from unicon import Connection
from unicon.settings import Settings

from genie.libs.clean.recovery.recovery import recovery_processor

import logging

logger = logging.getLogger(__name__)


class MockDisconnectReconnect:

    def __init__(self, *args, **kwargs):
        self.state = iter([False, False, True])

    def __call__(self, *arg, **kwargs):
        state = next(self.state)
        return state


mock_disconnect_reconnect =  MockDisconnectReconnect()


class TestRecovery(unittest.TestCase):

    @patch('genie.libs.clean.recovery.recovery._disconnect_reconnect', new=mock_disconnect_reconnect)
    def test_recovery_processor_telnet_break(self):
        section = Mock()
        section.parent = Mock()
        section.parent.history = ['Connect']
        section.parent.parameters = {}
        section.parameters = {}
        device = section.parameters['device'] = MagicMock()
        device.os = 'iosxe'
        device.is_ha = False
        device.custom = {'abstraction': {'order': ['os']}}
        device.cli.settings = Settings()
        device.cli.settings.ENV = {}
        device.start = ['mock_device_cli --os iosxe --state breakboot']
        device.api.verify_connectivity = Mock(return_value=False)
        device.cli.sendline('breakboot')
        device.log = logger
        recovery_processor(
            section,
            console_activity_pattern='Initializing Hardware',
            console_breakboot_telnet_break=True,
            break_count=1,
            golden_image=['bootflash:asr1000_golden.bin'],
            reconnect_delay=1)
        self.assertTrue(section.parent.parameters['block_section'])
