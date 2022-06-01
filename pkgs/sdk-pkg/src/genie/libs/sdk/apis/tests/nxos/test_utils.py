
import re
import unittest
from unittest.mock import MagicMock, Mock

from genie.libs.sdk.apis.nxos.aci.utils import (
    copy_from_device, copy_to_device)


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
