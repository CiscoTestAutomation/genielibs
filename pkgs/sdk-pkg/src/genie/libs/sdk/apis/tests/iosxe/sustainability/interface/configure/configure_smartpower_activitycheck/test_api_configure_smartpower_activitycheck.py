from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.interface.configure import (
    configure_smartpower_activitycheck,
)


class TestConfigureSmartpowerActivitycheck(TestCase):

    def test_configure_smartpower_activitycheck(self):
        device = Mock()

        result = configure_smartpower_activitycheck(device, 'Gi1/0/13')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ['interface Gi1/0/13', 'smartpower activitycheck']
        )
