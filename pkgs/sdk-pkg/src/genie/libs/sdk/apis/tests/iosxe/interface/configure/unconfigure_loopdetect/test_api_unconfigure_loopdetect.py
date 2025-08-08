from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_loopdetect
from unittest.mock import Mock


class TestUnconfigureLoopdetect(TestCase):

    def test_unconfigure_loopdetect(self):
        self.device = Mock()
        result = unconfigure_loopdetect(self.device, 'GigabitEthernet1/1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/1', 'no loopdetect'],)
        )
