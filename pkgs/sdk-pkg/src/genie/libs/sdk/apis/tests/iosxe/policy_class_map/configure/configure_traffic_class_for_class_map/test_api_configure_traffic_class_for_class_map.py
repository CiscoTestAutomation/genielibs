import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_class_map.configure import configure_traffic_class_for_class_map


class TestConfigureTrafficClassForClassMap(unittest.TestCase):

    def test_configure_traffic_class_for_class_map(self):
        device = Mock()

        result = configure_traffic_class_for_class_map(
            device,
            'tc7',
            'match-any',
            7
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'class-map match-any tc7',
                'match traffic-class 7'
            ],)
        )