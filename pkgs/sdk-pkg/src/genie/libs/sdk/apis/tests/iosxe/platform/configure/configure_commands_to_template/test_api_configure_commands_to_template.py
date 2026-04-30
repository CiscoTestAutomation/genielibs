from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_commands_to_template


class TestConfigureCommandsToTemplate(TestCase):

    def test_configure_commands_to_template(self):
        device = Mock()
        result = configure_commands_to_template(
            device,
            'hello_world',
            'switchport mode access'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['template hello_world', 'switchport mode access'],)
        )