from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.zone.configure import (
    unconfigure_zone_pair_security,
)


class TestUnconfigureZonePairSecurity(TestCase):

    def test_unconfigure_zone_pair_security(self):
        self.device = Mock()
        unconfigure_zone_pair_security(
            self.device, 'zone1_zone2', 'zone1', 'zone2',
            service_policy='pm',
        )
        self.device.configure.assert_called_once_with(
            [
                'zone-pair security zone1_zone2 source zone1 '
                'destination zone2',
                'no service-policy type inspect pm',
                'exit',
                'no zone-pair security zone1_zone2 source zone1 '
                'destination zone2',
            ]
        )

    def test_unconfigure_zone_pair_security_delete_only(self):
        self.device = Mock()
        unconfigure_zone_pair_security(
            self.device, 'zone1_zone2', 'zone1', 'zone2',
        )
        self.device.configure.assert_called_once_with(
            [
                'no zone-pair security zone1_zone2 source zone1 '
                'destination zone2',
            ]
        )

    def test_unconfigure_zone_pair_security_detach_only(self):
        self.device = Mock()
        unconfigure_zone_pair_security(
            self.device, 'zone1_zone2', 'zone1', 'zone2',
            service_policy='pm', remove_zone_pair=False,
        )
        self.device.configure.assert_called_once_with(
            [
                'zone-pair security zone1_zone2 source zone1 '
                'destination zone2',
                'no service-policy type inspect pm',
                'exit',
            ]
        )

    def test_unconfigure_zone_pair_security_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_zone_pair_security(
                self.device, 'zone1_zone2', 'zone1', 'zone2',
            )
