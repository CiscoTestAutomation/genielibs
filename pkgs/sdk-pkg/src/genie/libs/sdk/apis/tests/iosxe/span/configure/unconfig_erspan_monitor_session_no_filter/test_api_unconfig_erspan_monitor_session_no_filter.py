from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.span.configure import (
    unconfig_erspan_monitor_session_no_filter,
)


class TestUnconfigErspanMonitorSessionNoFilter(TestCase):

    def test_unconfig_erspan_monitor_session_no_filter(self):
        device = Mock()

        result = unconfig_erspan_monitor_session_no_filter(
            device,
            '1',
            '2333'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'monitor session 1 type erspan-source',
                    'no filter vlan 2333',
                ],
            )
        )
