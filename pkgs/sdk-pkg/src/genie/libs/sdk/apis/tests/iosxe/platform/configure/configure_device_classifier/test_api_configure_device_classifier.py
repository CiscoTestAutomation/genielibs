from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_device_classifier
from unittest.mock import Mock


class TestConfigureDeviceClassifier(TestCase):

    def test_configure_device_classifier(self):
        self.device = Mock()
        result = configure_device_classifier(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('device classifier',)
        )

    def test_configure_device_classifier_1(self):
        self.device = Mock()
        result = configure_device_classifier(self.device, 'some_option', 'some_value')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('device classifier some_option some_value',)
        )
