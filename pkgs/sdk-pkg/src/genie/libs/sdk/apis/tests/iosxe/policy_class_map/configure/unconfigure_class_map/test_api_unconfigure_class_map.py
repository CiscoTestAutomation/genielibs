import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_class_map.configure import unconfigure_class_map


class TestUnconfigureClassMap(unittest.TestCase):

    def test_unconfigure_class_map(self):
        device = Mock()

        result = unconfigure_class_map(
            device,
            'test1',
            'match-all'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no class-map match-all test1',)
        )