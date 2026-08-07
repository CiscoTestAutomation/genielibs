from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    configure_ecomode_optics,
)


class TestConfigureEcomodeOptics(TestCase):

    def test_configure_ecomode_optics(self):
        device = Mock()

        result = configure_ecomode_optics(device, '1')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'hw-module switch 1 ecomode optics'
        )
