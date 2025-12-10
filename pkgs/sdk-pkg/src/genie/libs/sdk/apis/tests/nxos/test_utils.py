
import re
import unittest
from unittest.mock import MagicMock, Mock, call, patch

from genie.libs.sdk.apis.nxos.aci.utils import (
    copy_from_device, copy_to_device)

from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.sdk.apis.nxos.utils import device_recovery_boot


class TestUtilsApi(unittest.TestCase):

    def test_copy_from_device_nxos_aci(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'nxos'
        device.platform = 'aci'
        device.via = 'cli'
        device.api.get_mgmt_src_ip_addresses = Mock(return_value=['127.0.0.1'])
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.execute = Mock()
        copy_from_device(device, local_path='/tmp/test.txt')
        assert re.search(r'curl --upload-file /tmp/test.txt -u \w+:\w+ http://127.0.0.1:\d+/router_test.txt', str(device.execute.call_args))

    def test_copy_to_device_nxos_aci(self):
        device = MagicMock()
        device.os = 'nxos'
        device.platform = 'aci'
        device.via = 'cli'
        device.api.get_mgmt_src_ip_addresses = Mock(return_value=['127.0.0.1'])
        device.api.get_local_ip = Mock(return_value='127.0.0.1')
        device.execute = Mock()
        copy_to_device(device, remote_path='/tmp/test.txt')
        assert re.search(r'curl -u \w+:\w+ http://127.0.0.1:\d+/test.txt -O', str(device.execute.call_args))

    def test_device_recovery_boot(self):
        device = create_test_device(name='aDevice', os='nxos')
        device.destroy = Mock()
        device.start = ['telnet 127.0.0.1 0000']
        device.instantiate = Mock()
        device.setup_connection = Mock()
        device.is_ha = False
        device.clean = {'device_recovery':
                            {'golden_image':{'system':'bootflash:packages.conf'},
                            'recovery_password':'lab'}}
        with patch("genie.libs.sdk.apis.nxos.utils.Lookup") as lookup_mock:
            with patch("genie.libs.sdk.apis.nxos.utils.pcall") as pcall_mock:
                lookup_clean = Mock()
                lookup_clean.clean.recovery.recovery.recovery_worker = Mock()
                lookup_mock.from_device.return_value = lookup_clean
                device_recovery_boot(device)
                expected_calls = [call(lookup_clean.clean.recovery.recovery.recovery_worker, start=device.start,ikwargs=[{'item': 0}], ckwargs={'device': device, 'console_activity_pattern': '\\.\\.\\.\\.', 'console_breakboot_char': '\x03',
                                  'console_breakboot_telnet_break': False, 'grub_activity_pattern': None, 'grub_breakboot_char': 'c', 'break_count': 15, 'timeout': 750, 'golden_image': {'system': 'bootflash:packages.conf'}, 'tftp_boot': None, 'recovery_password': 'lab'})]
                self.assertEqual(pcall_mock.mock_calls, expected_calls)
                pcall_mock.assert_called_once()