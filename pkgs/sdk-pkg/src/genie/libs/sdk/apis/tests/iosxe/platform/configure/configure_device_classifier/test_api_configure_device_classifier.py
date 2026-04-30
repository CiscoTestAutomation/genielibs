from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_device_classifier


class TestConfigureDeviceClassifier(TestCase):

    def test_configure_device_classifier(self):
        device = Mock()
        result = configure_device_classifier(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('device classifier',)
        )

    def test_configure_device_classifier_1(self):
        device = Mock()
        result = configure_device_classifier(
            device,
            'some_option',
            'some_value'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('device classifier some_option some_value',)
        )