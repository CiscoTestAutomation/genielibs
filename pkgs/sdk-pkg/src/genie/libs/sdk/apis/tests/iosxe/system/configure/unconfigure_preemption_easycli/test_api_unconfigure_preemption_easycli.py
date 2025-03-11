from unittest import TestCase
from genie.libs.sdk.apis.iosxe.system.configure import unconfigure_preemption_easycli
from unittest.mock import Mock


class TestUnconfigurePreemptionEasycli(TestCase):

    def test_unconfigure_preemption_easycli(self):
        self.device = Mock()
        result = unconfigure_preemption_easycli(self.device, 'cos', '2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no preemption cos 2',)
        )
