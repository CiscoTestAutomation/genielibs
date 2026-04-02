from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat_translation_max_entries

class TestUnconfigureNatTranslationMaxEntries(TestCase):

    def test_unconfigure_nat_translation_max_entries(self):
        device = Mock()
        result = unconfigure_nat_translation_max_entries(device, 'vrf', 'test', 5)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat translation max-entries vrf test 5',)
        )

    def test_unconfigure_nat_translation_max_entries_1(self):
        device = Mock()
        result = unconfigure_nat_translation_max_entries(device, 'all-vrf', '', 5)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat translation max-entries all-vrf  5',)
        )

    def test_unconfigure_nat_translation_max_entries_2(self):
        device = Mock()
        result = unconfigure_nat_translation_max_entries(device, 'list', 'test1', 5)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat translation max-entries list test1 5',)
        )