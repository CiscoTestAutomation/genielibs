from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.zone.configure import (
    unconfigure_zone_member_security,
)


class TestUnconfigureZoneMemberSecurity(TestCase):

    def test_unconfigure_zone_member_security(self):
        self.device = Mock()
        unconfigure_zone_member_security(
            self.device, 'GigabitEthernet0/1/2', 'zone1',
        )
        self.device.configure.assert_called_once_with(
            [
                'interface GigabitEthernet0/1/2',
                'no zone-member security zone1',
            ]
        )

    def test_unconfigure_zone_member_security_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_zone_member_security(
                self.device, 'GigabitEthernet0/1/2', 'zone1',
            )
