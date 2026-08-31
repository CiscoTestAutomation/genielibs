from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vdsl.configure import (
    configure_controller_shutdown,
)


class TestConfigureControllerShutdown(TestCase):

    def test_configure_controller_shutdown(self):
        device = Mock()

        result = configure_controller_shutdown(
            device,
            '0/0/0',
            shutdown=False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'Controller VDSL 0/0/0\n'
            'no shutdown'
        )
