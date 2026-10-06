import os
import unittest
from unittest.mock import MagicMock

from pyats.topology import loader

from genie.libs.sdk.apis.iosxr.platform.get import get_available_space
from genie.metaparser.util.exceptions import SchemaEmptyParserError, SchemaMissingKeyError


class TestGetAvailableSpace(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          R2_xr:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxr --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxr
            platform: iosxrv9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R2_xr']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_available_space(self):
        result = get_available_space(self.device)
        expected_output = 933916000
        self.assertEqual(result, expected_output)

    def test_empty_directory_parse_returns_none(self):
        device = MagicMock()
        device.parse.side_effect = SchemaEmptyParserError(data={}, command='dir harddisk:')

        result = get_available_space(device, directory='harddisk:')

        self.assertIsNone(result)
        device.parse.assert_called_once_with('dir harddisk:', output=None)

    def test_missing_key_parse_returns_none(self):
        device = MagicMock()
        device.parse.side_effect = SchemaMissingKeyError(path=[], keys=['total_free_bytes'], command='dir harddisk:')

        result = get_available_space(device, directory='harddisk:')

        self.assertIsNone(result)

    def test_missing_free_space_value_returns_none(self):
        device = MagicMock()
        device.parse.return_value = {'dir': {'dir_name': 'harddisk:'}}

        result = get_available_space(device, directory='harddisk:')

        self.assertIsNone(result)
