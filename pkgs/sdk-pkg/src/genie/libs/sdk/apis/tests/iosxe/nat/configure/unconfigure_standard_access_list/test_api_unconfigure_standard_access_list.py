from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_standard_access_list

class TestUnconfigureStandardAccessList(TestCase):

    def test_unconfigure_standard_access_list(self):
        device = Mock()
        result = unconfigure_standard_access_list(device, '11', 'permit', 'any', None)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no access-list 11 permit any'],)
        )