from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfig_preemption
from unittest.mock import Mock


class TestUnconfigPreemption(TestCase):

    def test_unconfig_preemption(self):
        self.device = Mock()
        result = unconfig_preemption(self.device, 'gig1/4')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface gig1/4', 'no preemption-enable'],)
        )
