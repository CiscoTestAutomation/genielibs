from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_manual
from unittest.mock import Mock


class TestUnconfigureCtsManual(TestCase):

    def test_unconfigure_cts_manual(self):
        self.device = Mock()
        result = unconfigure_cts_manual(self.device, 'HundredGigE1/0/23')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface HundredGigE1/0/23', 'no cts manual'],)
        )
