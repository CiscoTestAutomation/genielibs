from unittest import TestCase
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_standard_access_list
from unittest.mock import Mock


class TestUnconfigureStandardAccessList(TestCase):

    def test_unconfigure_standard_access_list(self):
        self.device = Mock()
        result = unconfigure_standard_access_list(self.device, '11', 'permit', 'any', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no access-list 11 permit any'],)
        )
