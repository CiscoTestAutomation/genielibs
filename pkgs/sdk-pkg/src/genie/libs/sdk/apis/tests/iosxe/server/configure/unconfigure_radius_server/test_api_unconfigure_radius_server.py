from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.server.configure import unconfigure_radius_server


class TestUnconfigureRadiusServer(TestCase):

    def test_unconfigure_radius_server(self):
        device = Mock()

        result = unconfigure_radius_server(device, 'radius_server')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no radius server radius_server',
        )
