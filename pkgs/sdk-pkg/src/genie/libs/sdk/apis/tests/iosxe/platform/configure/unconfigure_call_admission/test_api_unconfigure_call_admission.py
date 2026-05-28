import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_call_admission


class TestUnconfigureCallAdmission(unittest.TestCase):

    def test_unconfigure_call_admission(self):
        device = Mock()

        result = unconfigure_call_admission(device, 600, 80, 1, 10)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'no call admission new-model',
                'no call admission limit 600',
                'no call admission cpu-limit 80',
                'no call admission pppoe 1 10',
                'no call admission vpdn 10 1'
            ],)
        )