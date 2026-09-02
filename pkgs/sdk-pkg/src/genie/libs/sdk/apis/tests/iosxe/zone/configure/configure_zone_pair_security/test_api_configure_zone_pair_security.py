from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.zone.configure import (
    configure_zone_pair_security,
)


class TestConfigureZonePairSecurity(TestCase):

    def test_configure_zone_pair_security(self):
        self.device = Mock()
        configure_zone_pair_security(
            self.device, 'zone1_zone2', 'zone1', 'zone2',
            service_policy='pm',
        )
        self.device.configure.assert_called_once_with(
            [
                'zone-pair security zone1_zone2 source zone1 '
                'destination zone2',
                'service-policy type inspect pm',
            ]
        )

    def test_configure_zone_pair_security_no_policy(self):
        self.device = Mock()
        configure_zone_pair_security(
            self.device, 'zone1_zone2', 'zone1', 'zone2',
        )
        self.device.configure.assert_called_once_with(
            [
                'zone-pair security zone1_zone2 source zone1 '
                'destination zone2',
            ]
        )

    def test_configure_zone_pair_security_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_zone_pair_security(
                self.device, 'zone1_zone2', 'zone1', 'zone2',
            )
