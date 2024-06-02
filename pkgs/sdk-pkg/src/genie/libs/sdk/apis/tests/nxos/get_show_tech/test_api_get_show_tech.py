import unittest
from unittest.mock import Mock, call, ANY
from pyats.topology import loader


class TestGetShowTech(unittest.TestCase):

    def test_get_show_tech(self):
        tb = loader.load('testbed.yaml')
        dev = tb.devices.SW1
        dev.connect = Mock()
        dev.execute = Mock()
        result = dev.api.get_show_tech(remote_server='scp-1', remote_path='/tmp')
        self.assertIn('use-kstack', dev.execute.call_args_list[3][0][0])
