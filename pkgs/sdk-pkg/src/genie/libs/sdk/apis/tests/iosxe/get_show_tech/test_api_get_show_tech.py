import unittest
from pyats.topology import loader


class TestGetShowTech(unittest.TestCase):

    def test_get_show_tech(self):
        tb = loader.load('testbed.yaml')
        dev = tb.devices.Router
        dev.connect(mit=True)
        result = dev.api.get_show_tech(remote_server='scp-1', remote_path='/tmp')
        self.assertTrue(result)
