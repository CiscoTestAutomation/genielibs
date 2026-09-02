from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.table_map.configure import (
    configure_table_map_set_default,
)


class TestConfigureTableMapSetDefault(TestCase):

    def test_configure_table_map_set_default(self):
        device = Mock()

        result = configure_table_map_set_default(device, 'cos2cos', 'copy')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ['table-map cos2cos', 'default copy']
        )
