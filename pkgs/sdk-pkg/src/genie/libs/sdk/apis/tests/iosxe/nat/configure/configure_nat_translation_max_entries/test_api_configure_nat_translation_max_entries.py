from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat_translation_max_entries

class TestConfigureNatTranslationMaxEntries(TestCase):

    def test_configure_nat_translation_max_entries(self):
        device = Mock()
        result = configure_nat_translation_max_entries(device, 'vrf', 'test', 5)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip nat translation max-entries vrf test 5',)
        )

    def test_configure_nat_translation_max_entries_1(self):
        device = Mock()
        result = configure_nat_translation_max_entries(device, 'all-vrf', '', 5)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip nat translation max-entries all-vrf  5',)  # note double space
        )

    def test_configure_nat_translation_max_entries_2(self):
        device = Mock()
        result = configure_nat_translation_max_entries(device, 'list', 'test1', 4)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip nat translation max-entries list test1 4',)
        )