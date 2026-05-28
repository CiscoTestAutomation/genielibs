import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_device_classifier_profile


class TestUnconfigureDeviceClassifierProfile(unittest.TestCase):

    def test_unconfigure_device_classifier_profile(self):
        device = Mock()

        result = unconfigure_device_classifier_profile(
            device,
            'condition',
            'COND_TEST_A',
            'no lldp',
            'tlv-type 6 value String Cisco',
            'no device classifier',
            'condition',
            'CDP_RULE_TLV_1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'no device classifier',
                'device classifier condition COND_TEST_A',
                'no lldp tlv-type 6 value String Cisco',
                'no device classifier condition CDP_RULE_TLV_1'
            ],)
        )