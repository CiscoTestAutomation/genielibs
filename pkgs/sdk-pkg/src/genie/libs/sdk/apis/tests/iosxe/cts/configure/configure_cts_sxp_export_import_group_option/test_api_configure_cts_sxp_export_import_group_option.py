from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_sxp_export_import_group_option
from unittest.mock import Mock


class TestConfigureCtsSxpExportImportGroupOption(TestCase):

    def test_configure_cts_sxp_export_import_group_option(self):
        self.device = Mock()
        result = configure_cts_sxp_export_import_group_option(self.device, 'listener', 'Listener_GRP_DUT1', 'import-list', 'Import_List_DUT2', None, '2001:1122:AABB:2:DDEE:77CC:4321:1111')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['cts sxp export-import-group listener Listener_GRP_DUT1', 'import-list Import_List_DUT2', 'peer-ipv6 2001:1122:AABB:2:DDEE:77CC:4321:1111'],)
        )
