from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_event_manager


class TestConfigureEventManager(TestCase):

    def test_configure_event_manager(self):
        device = Mock()
        result = configure_event_manager(
            device,
            'RELOAD',
            'RELOAD',
            'sync',
            'yes',
            'cli',
            'reload'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'event manager applet RELOAD',
                'description RELOAD',
                'event none sync yes',
                'action cli reload'
            ],)
        )