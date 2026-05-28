import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_source_template


class TestConfigureSourceTemplate(unittest.TestCase):

    def test_configure_source_template(self):
        device = Mock()

        result = configure_source_template(device, 'hello_world', 'a')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['template hello_world', 'source template a'],)
        )