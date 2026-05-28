from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_flow_monitor_cache_inactive_timeout
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure


class TestConfigureFlowMonitorCacheInactiveTimeout(TestCase):

    def test_configure_flow_monitor_cache_inactive_timeout(self):
        self.device = Mock()
        result = configure_flow_monitor_cache_inactive_timeout(self.device, 'wdavc', '20')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['flow monitor wdavc', 'cache timeout inactive 20'],)
        )

    def test_configure_flow_monitor_cache_inactive_timeout_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('configure failed')
        with self.assertRaises(SubCommandFailure) as cm:
            configure_flow_monitor_cache_inactive_timeout(self.device, 'wdavc', '20')
        self.assertIn(
            'Could not configure cache timeout inactive on flow monitor wdavc',
            str(cm.exception)
        )
