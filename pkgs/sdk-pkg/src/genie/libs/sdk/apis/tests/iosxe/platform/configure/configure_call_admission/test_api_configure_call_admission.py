from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_call_admission


class TestConfigureCallAdmission(TestCase):

    def test_configure_call_admission(self):
        device = Mock()
        result = configure_call_admission(
            device,
            600,
            80,
            1,
            10
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'call admission new-model',
                'call admission limit 600',
                'call admission cpu-limit 80',
                'call admission pppoe 1 10',
                'call admission vpdn 10 1'
            ],)
        )