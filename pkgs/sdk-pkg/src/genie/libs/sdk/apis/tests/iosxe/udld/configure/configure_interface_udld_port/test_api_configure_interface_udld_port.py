from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.udld.configure import (
    configure_interface_udld_port,
)


class TestConfigureInterfaceUdldPort(TestCase):

    def test_configure_interface_udld_port(self):
        device = Mock()

        result = configure_interface_udld_port(
            device,
            'Tw1/0/4',
            aggressive_mode=True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface Tw1/0/4',
                'udld port aggressive',
            ]
        )
