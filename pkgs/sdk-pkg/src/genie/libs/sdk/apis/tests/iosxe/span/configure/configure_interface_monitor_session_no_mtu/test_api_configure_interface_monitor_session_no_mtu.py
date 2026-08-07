from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.span.configure import (
    configure_interface_monitor_session_no_mtu,
)


class TestConfigureInterfaceMonitorSessionNoMtu(TestCase):

    def test_configure_interface_monitor_session_no_mtu(self):
        device = Mock()

        result = configure_interface_monitor_session_no_mtu(
            device,
            '2',
            '1500'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
             (['monitor session 2 type erspan-source', 'destination', 'no mtu 1500'],)
        )
