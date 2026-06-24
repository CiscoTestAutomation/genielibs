from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.subscriber.clear import clear_subscriber_session_all
from unicon.core.errors import SubCommandFailure


class TestClearSubscriberSessionAll(TestCase):

    def test_clear_subscriber_session_all(self):
        self.device = Mock()
        self.device.execute.return_value = ''
        clear_subscriber_session_all(self.device)
        self.assertIn(
            'clear subscriber session all',
            self.device.execute.call_args_list[0][0]
        )

    def test_clear_subscriber_session_all_failure(self):
        self.device = Mock()
        self.device.execute.side_effect = SubCommandFailure('Test error')
        with self.assertRaises(SubCommandFailure):
            clear_subscriber_session_all(self.device)
