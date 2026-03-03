from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_sxp_export_import_group_option
from unittest.mock import Mock


class TestUnconfigureCtsSxpExportImportGroupOption(TestCase):

    def test_unconfigure_cts_sxp_export_import_group_option(self):
        self.device = Mock()
        result = unconfigure_cts_sxp_export_import_group_option(self.device, 'speaker', 'Speaker_GRP_DUT1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts sxp export-import-group speaker Speaker_GRP_DUT1'],)
        )
