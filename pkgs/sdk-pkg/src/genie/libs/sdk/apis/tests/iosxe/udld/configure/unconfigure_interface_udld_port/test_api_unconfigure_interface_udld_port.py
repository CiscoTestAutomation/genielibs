from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.udld.configure import (
    unconfigure_interface_udld_port,
)


class TestUnconfigureInterfaceUdldPort(TestCase):

    def test_unconfigure_interface_udld_port(self):
        device = Mock()

        result = unconfigure_interface_udld_port(
            device,
            'Tw1/0/4',
            aggressive_mode=True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface Tw1/0/4',
                'no udld port aggressive',
            ]
        )
