from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.execute import configure_autolc_shutdown_priority
from unittest.mock import Mock


class TestConfigureAutolcShutdownPriority(TestCase):

    def test_configure_autolc_shutdown_priority(self):
        self.device = Mock()
        result = configure_autolc_shutdown_priority(self.device, '10 9 8 7 4 3 2 1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('power supply autoLC priority 10 9 8 7 4 3 2 1',)
        )
