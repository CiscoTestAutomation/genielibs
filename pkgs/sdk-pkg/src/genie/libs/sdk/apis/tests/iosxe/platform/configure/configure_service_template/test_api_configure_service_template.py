import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_service_template


class TestConfigureServiceTemplate(unittest.TestCase):

    def test_configure_service_template(self):
        device = Mock()

        result = configure_service_template(device, 'test')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('service-template test',)
        )