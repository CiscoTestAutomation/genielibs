from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.span.configure import (
    config_erspan_monitor_session_shut_unshut,
)


class TestConfigErspanMonitorSessionShutUnshut(TestCase):

    def test_config_erspan_monitor_session_shut_unshut(self):
        device = Mock()

        result = config_erspan_monitor_session_shut_unshut(
            device,
            '1',
            'shutdown'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['monitor session 1 type erspan-source', 'shutdown'],)
        )
