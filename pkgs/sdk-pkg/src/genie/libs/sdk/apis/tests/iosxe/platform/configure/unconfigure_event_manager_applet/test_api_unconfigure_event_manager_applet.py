import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_event_manager_applet


class TestUnconfigureEventManagerApplet(unittest.TestCase):

    def test_unconfigure_event_manager_applet(self):
        device = Mock()

        result = unconfigure_event_manager_applet(device, 'test')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no event manager applet test',)
        )