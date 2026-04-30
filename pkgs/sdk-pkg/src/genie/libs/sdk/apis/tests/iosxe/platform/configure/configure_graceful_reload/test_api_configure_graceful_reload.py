from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_graceful_reload


class TestConfigureGracefulReload(TestCase):

    def test_configure_graceful_reload(self):
        device = Mock()
        result = configure_graceful_reload(
            device,
            '5'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('graceful-reload interval 5',)
        )