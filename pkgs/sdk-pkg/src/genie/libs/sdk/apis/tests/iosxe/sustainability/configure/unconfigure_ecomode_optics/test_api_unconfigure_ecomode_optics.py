from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    unconfigure_ecomode_optics,
)


class TestUnconfigureEcomodeOptics(TestCase):

    def test_unconfigure_ecomode_optics(self):
        device = Mock()

        result = unconfigure_ecomode_optics(device, '1')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no hw-module switch 1 ecomode optics'
        )
