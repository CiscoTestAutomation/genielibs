from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.span.configure import (
    unconfig_erspan_monitor_session_no_source,
)


class TestUnconfigErspanMonitorSessionNoSource(TestCase):

    def test_unconfig_erspan_monitor_session_no_source(self):
        device = Mock()

        result = unconfig_erspan_monitor_session_no_source(
            device,
            '1',
            '',
            '2333'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'monitor session 1  type erspan-source',
                    'no source vlan 2333',
                ],
            )
        )
