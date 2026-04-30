from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_archive_default


class TestConfigureArchiveDefault(TestCase):

    def test_configure_archive_default(self):
        device = Mock()
        result = configure_archive_default(
            device,
            'rollback',
            'filter'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['archive', 'default rollback filter adaptive'],)
        )