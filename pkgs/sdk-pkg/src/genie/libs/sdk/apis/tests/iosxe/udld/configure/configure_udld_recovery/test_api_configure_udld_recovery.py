from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.udld.configure import (
    configure_udld_recovery,
)


class TestConfigureUdldRecovery(TestCase):

    def test_configure_udld_recovery(self):
        device = Mock()

        result = configure_udld_recovery(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(['udld recovery'])
