from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.udld.configure import (
    unconfigure_udld_recovery,
)


class TestUnconfigureUdldRecovery(TestCase):

    def test_unconfigure_udld_recovery(self):
        device = Mock()

        result = unconfigure_udld_recovery(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no udld recovery')
