from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_loopdetect
from unittest.mock import Mock


class TestConfigureLoopdetect(TestCase):

    def test_configure_loopdetect(self):
        self.device = Mock()
        result = configure_loopdetect(self.device, 'GigabitEthernet1/1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/1', 'loopdetect'],)
        )
