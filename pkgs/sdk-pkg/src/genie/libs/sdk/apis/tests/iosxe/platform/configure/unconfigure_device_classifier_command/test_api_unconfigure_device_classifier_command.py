import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_device_classifier_command


class TestUnconfigureDeviceClassifierCommand(unittest.TestCase):

    def test_unconfigure_device_classifier_command(self):
        device = Mock()

        result = unconfigure_device_classifier_command(
            device,
            'condition',
            'COND_TEST_A',
            'no lldp',
            'tlv-type 6 value String Cisco'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'no device classifier',
                'device classifier condition COND_TEST_A',
                'no lldp tlv-type 6 value String Cisco'
            ],)
        )