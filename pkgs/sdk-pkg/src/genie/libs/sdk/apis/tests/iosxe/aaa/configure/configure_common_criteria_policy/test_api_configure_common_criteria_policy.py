import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_common_criteria_policy


class TestConfigureCommonCriteriaPolicy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_common_criteria_policy(self):
        configure_common_criteria_policy(self.device, 'ABCD', None, None, None, None, None, None, 1, None, None, None, False, None)
        self.device.configure.assert_called_with([
            'aaa common-criteria policy ABCD'
        ])

    def test_configure_common_criteria_policy_1(self):
        configure_common_criteria_policy(self.device, 'CDEF', 5, None, None, 1, 1, 20, 8, None, 1, 5, True, 1)
        self.device.configure.assert_called_with([
            'aaa common-criteria policy CDEF',
            'char-changes 5',
            'lower-case 1',
            'upper-case 1',
            'max-length 20',
            'min-length 8',
            'numeric-count 1',
            'special-case 1',
            'character-repetition 5',
            'restrict-consecutive-letters'
        ])
