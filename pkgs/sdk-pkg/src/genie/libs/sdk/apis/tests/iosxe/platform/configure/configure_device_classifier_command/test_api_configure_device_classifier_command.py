from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_device_classifier_command


class TestConfigureDeviceClassifierCommand(TestCase):

    def test_configure_device_classifier_command(self):
        device = Mock()
        result = configure_device_classifier_command(
            device,
            'condition',
            'COND_TEST_A',
            'no lldp',
            'tlv-type 6 value String Cisco',
            'no device classifier',
            30
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'device classifier condition COND_TEST_A',
                'no lldp tlv-type 6 value String Cisco',
                'no device classifier'
            ],)
        )