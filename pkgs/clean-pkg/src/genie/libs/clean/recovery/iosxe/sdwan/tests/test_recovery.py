import unittest
from unittest.mock import MagicMock, Mock, patch

from genie.libs.clean.recovery.iosxe.sdwan.recovery import recovery_worker


class TestRecoveryWorker(unittest.TestCase):

    @patch('genie.libs.clean.recovery.iosxe.sdwan.recovery.device_recovery')
    @patch('genie.libs.clean.recovery.iosxe.sdwan.recovery.BreakBootDialog')
    @patch('genie.libs.clean.recovery.iosxe.sdwan.recovery.Spawn')
    def test_legacy_dispatcher_derives_start_after_instantiate(
            self, spawn_cls, break_dialog_cls, device_recovery):
        device = MagicMock()
        device.name = 'aDevice'
        device.hostname = 'aDevice'
        device.start = 'telnet 127.0.0.1 0000'
        device.cli.settings = {}
        device.instantiate = Mock()

        recovery_worker(device=device, golden_image=['bootflash:image.bin'])

        device.instantiate.assert_called_once_with(connection_timeout=600)
        spawn_cls.assert_called_once_with(
            spawn_command='telnet 127.0.0.1 0000',
            settings={},
            target='aDevice_0000',
            log=unittest.mock.ANY,
            logfile=None)
        device_recovery.assert_called_once()
        spawn_cls.return_value.close.assert_called_once_with()
