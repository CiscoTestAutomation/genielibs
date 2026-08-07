from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.span.configure import (
    configure_interface_monitor_session_shutdown_erspan_dest,
)


class TestConfigureInterfaceMonitorSessionShutdownErspanDest(TestCase):

    def test_configure_interface_monitor_session_shutdown_erspan_dest(self):
        device = Mock()

        result = configure_interface_monitor_session_shutdown_erspan_dest(
            device,
            '2'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['monitor session 2 type erspan-destination', 'shutdown'],)
        )
