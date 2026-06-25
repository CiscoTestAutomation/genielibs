import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_policy_map_class_parameters
)


class TestConfigurePolicyMapClassParameters(unittest.TestCase):

    def test_configure_policy_map_class_parameters(self):
        device = Mock()

        result = configure_policy_map_class_parameters(
            device, 'test', 'test', 200000, None, None, None, None,
            'set-discard-class-transmit', 5, 60000000,
            'set-discard-class-transmit', 5, 'set-dscp-transmit',
            'dscp', 't1', None, None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map test',
              'class test',
              'police 200000 pir 60000000 conform-action set-discard-class-transmit 5 exceed-action set-discard-class-transmit 5 violate-action set-dscp-transmit dscp table t1'],)
        )

    def test_configure_policy_map_class_parameters_1(self):
        device = Mock()

        result = configure_policy_map_class_parameters(
            device, 'test', 'test', None, None, 30, None, None,
            'transmit', None, None, None, None, 'set-dscp-transmit',
            'dscp', None, None, None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map test',
              'class test',
              'police cir percent 30 conform-action transmit'],)
        )

    def test_configure_policy_map_class_parameters_2(self):
        device = Mock()

        result = configure_policy_map_class_parameters(
            device, 'test', 'test', None, None, None, None, 20,
            'set-discard-class-transmit', 5, None, 'transmit',
            None, 'set-dscp-transmit', 'dscp', 't1', None, None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map test',
              'class test',
              'police rate percent 20 conform-action set-discard-class-transmit 5 exceed-action transmit violate-action set-dscp-transmit dscp table t1'],)
        )