from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.subscriber.execute import execute_show_subscriber_session_feature
from unicon.core.errors import SubCommandFailure


class TestExecuteShowSubscriberSessionFeature(TestCase):

    def test_execute_show_subscriber_session_feature(self):
        self.device = Mock()
        self.device.execute.return_value = 'feature output'
        result = execute_show_subscriber_session_feature(self.device, 'l4redirect')
        self.device.execute.assert_called_once_with(
            "show subscriber session feature l4redirect"
        )
        self.assertEqual(result, 'feature output')

    def test_execute_show_subscriber_session_feature_failure(self):
        self.device = Mock()
        self.device.execute.side_effect = SubCommandFailure('Test error')
        with self.assertRaises(SubCommandFailure):
            execute_show_subscriber_session_feature(self.device, 'l4redirect')
