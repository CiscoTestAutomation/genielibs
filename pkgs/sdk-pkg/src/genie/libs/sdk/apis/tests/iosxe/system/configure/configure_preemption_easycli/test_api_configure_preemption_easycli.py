from unittest import TestCase
from genie.libs.sdk.apis.iosxe.system.configure import configure_preemption_easycli
from unittest.mock import Mock


class TestConfigurePreemptionEasycli(TestCase):

    def test_configure_preemption_easycli(self):
        self.device = Mock()
        result = configure_preemption_easycli(self.device, 'cos', '2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('preemption cos 2',)
        )
