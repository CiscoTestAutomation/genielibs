import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_commands_from_template


class TestUnconfigureCommandsFromTemplate(unittest.TestCase):

    def test_unconfigure_commands_from_template(self):
        device = Mock()

        result = unconfigure_commands_from_template(
            device, 'hello_world', 'switchport mode access'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['template hello_world', 'no switchport mode access'],)
        )