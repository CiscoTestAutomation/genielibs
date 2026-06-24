import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_table_map_on_device
)


class TestConfigureTableMapOnDevice(unittest.TestCase):

    def test_configure_table_map_on_device(self):
        device = Mock()

        result = configure_table_map_on_device(
            device,
            'tb1',
            1,
            3,
            'copy'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['table-map tb1',
              'map from 1 to 3',
              'default copy'],)
        )