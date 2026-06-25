import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_source_template_global


class TestUnconfigureSourceTemplateGlobal(unittest.TestCase):

    def test_unconfigure_source_template_global(self):
        device = Mock()

        result = unconfigure_source_template_global(
            device,
            'Parent',
            'Child'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['template Parent', 'no source template Child'],)
        )