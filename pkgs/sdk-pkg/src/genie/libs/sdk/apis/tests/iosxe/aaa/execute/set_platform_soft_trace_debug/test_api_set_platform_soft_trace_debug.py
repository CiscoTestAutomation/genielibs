import unittest
from genie.libs.sdk.apis.iosxe.aaa.execute import set_platform_soft_trace_debug


class TestSetPlatformSoftTraceDebug(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = unittest.mock.Mock()

    def test_set_platform_soft_trace_debug(self):
        set_platform_soft_trace_debug(self.device, 'smd', 'active', 'r0', 'aaa-acct', 'debug', 'switch')
        self.assertIn(
            'set platform software trace smd switch active r0 aaa-acct debug',
            self.device.execute.call_args[0])

    def test_set_platform_soft_trace_debug_1(self):
        set_platform_soft_trace_debug(self.device, 'smd', 'active', 'r0', 'aaa-acct', 'debug')
        self.assertIn(
            'set platform software trace smd r0 aaa-acct debug',
            self.device.execute.call_args[0])
