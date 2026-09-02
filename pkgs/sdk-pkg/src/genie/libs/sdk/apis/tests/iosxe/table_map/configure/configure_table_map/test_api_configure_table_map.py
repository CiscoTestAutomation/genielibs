from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.table_map.configure import (
    configure_table_map,
)


class TestConfigureTableMap(TestCase):

    def test_configure_table_map(self):
        device = Mock()

        result = configure_table_map(
            device=device,
            table_map_name='table_cos',
            from_val=['2', '5'],
            to_val=['5', '2'],
            default_val='copy',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'table-map table_cos',
                'map from 2 to 5',
                'map from 5 to 2',
                'default copy',
            ]
        )
