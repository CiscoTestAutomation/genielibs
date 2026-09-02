from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.zone.configure import configure_zone_security


class TestConfigureZoneSecurity(TestCase):

    def test_configure_zone_security_single(self):
        self.device = Mock()
        configure_zone_security(self.device, 'zone1')
        self.device.configure.assert_called_once_with(
            ['zone security zone1']
        )

    def test_configure_zone_security_list(self):
        self.device = Mock()
        configure_zone_security(self.device, ['zone1', 'zone2'])
        self.device.configure.assert_called_once_with(
            ['zone security zone1', 'zone security zone2']
        )

    def test_configure_zone_security_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_zone_security(self.device, 'zone1')
