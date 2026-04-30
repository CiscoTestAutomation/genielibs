from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_graceful_reload_interval


class TestConfigureGracefulReloadInterval(TestCase):

    def test_configure_graceful_reload_interval(self):
        device = Mock()
        result = configure_graceful_reload_interval(
            device,
            '10'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('graceful-reload interval 10',)
        )