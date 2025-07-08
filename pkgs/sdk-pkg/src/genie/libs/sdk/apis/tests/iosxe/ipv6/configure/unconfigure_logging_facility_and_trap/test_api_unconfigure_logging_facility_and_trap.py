from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import unconfigure_logging_facility_and_trap
from unittest.mock import Mock


class TestUnconfigureLoggingFacilityAndTrap(TestCase):

    def test_unconfigure_logging_facility_and_trap(self):
        self.device = Mock()
        result = unconfigure_logging_facility_and_trap(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no logging facility local0', 'no logging trap debugging'],)
        )
