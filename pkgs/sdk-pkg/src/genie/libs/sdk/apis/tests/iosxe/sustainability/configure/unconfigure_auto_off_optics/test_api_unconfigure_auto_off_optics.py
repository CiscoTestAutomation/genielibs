from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    unconfigure_auto_off_optics,
)


class TestUnconfigureAutoOffOptics(TestCase):

    def test_unconfigure_auto_off_optics(self):
        device = Mock()

        result = unconfigure_auto_off_optics(device, '1')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no hw-module switch 1 auto-off optics'
        )
