import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_class_map.configure import configure_class_map


class TestConfigureClassMap(unittest.TestCase):

    def test_configure_class_map(self):
        device = Mock()

        result = configure_class_map(
            device,
            'test1',
            'cs1',
            'dscp',
            '',
            '',
            'match-all',
            False
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['class-map match-all test1', 'match dscp  cs1'],)
        )