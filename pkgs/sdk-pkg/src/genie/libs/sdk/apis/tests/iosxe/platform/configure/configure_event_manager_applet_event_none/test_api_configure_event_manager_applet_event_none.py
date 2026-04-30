from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_event_manager_applet_event_none


class TestConfigureEventManagerAppletEventNone(TestCase):

    def test_configure_event_manager_applet_event_none(self):
        device = Mock()
        result = configure_event_manager_applet_event_none(
            device,
            'testapplet'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['event manager applet testapplet', 'event none'],)
        )