from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_bulkstat_profile


class TestConfigureBulkstatProfile(TestCase):

    def test_configure_bulkstat_profile(self):
        device = Mock()
        result = configure_bulkstat_profile(
            device,
            'Mohamed'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['bulkstat profile Mohamed'],)
        )