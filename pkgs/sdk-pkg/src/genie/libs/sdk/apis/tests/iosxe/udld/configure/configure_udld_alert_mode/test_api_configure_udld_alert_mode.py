from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.udld.configure import (
    configure_udld_alert_mode,
)


class TestConfigureUdldAlertMode(TestCase):

    def test_configure_udld_alert_mode(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_udld_alert_mode(
            device,
            'GigabitEthernet3/0/1',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface GigabitEthernet3/0/1',
                'udld port alert',
            ]
        )
