from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.span.configure import (
    config_erspan_monitor_session_filter,
)


class TestConfigErspanMonitorSessionFilter(TestCase):

    def test_config_erspan_monitor_session_filter(self):
        device = Mock()

        result = config_erspan_monitor_session_filter(
            device,
            '1',
            '2333'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['monitor session 1 type erspan-source', 'filter vlan 2333'],)
        )
