from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import config_preemption
from unittest.mock import Mock


class TestConfigPreemption(TestCase):

    def test_config_preemption(self):
        self.device = Mock()
        result = config_preemption(self.device, 'gig1/4')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface gig1/4', 'preemption-enable'],)
        )
