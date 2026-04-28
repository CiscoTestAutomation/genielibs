from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_archive_maximum


class TestConfigureArchiveMaximum(TestCase):

    def test_configure_archive_maximum(self):
        device = Mock()
        result = configure_archive_maximum(
            device,
            14
        )
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['archive', 'maximum 14'],)
        )