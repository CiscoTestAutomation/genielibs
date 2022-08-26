import unittest
from unittest.mock import Mock
from genie.conf import Genie
from genie.libs.sdk.apis.ios.platform.verify import verify_file_exists
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyFileExists(unittest.TestCase):

    parsed_outputs = {
        'dir bootflash:/': {
            'dir': {
                'bootflash:/': {
                    'files': {
                        'packages.conf': {'index': '1'}
                    }
                },
                'dir': 'bootflash:/'
            }
        },
        'dir bootflash:/empty_folder/': {
            'dir': {
                    'bootflash:/empty_folder/': {},
                    'dir': 'bootflash:/empty_folder/'
            }
        },
        'dir bootflash:/not_existing_folder/': {}
    }

    @classmethod
    def get_parsed_output(cls, arg, **kwargs):
        '''Return the parsed output of the given command '''
        return cls.parsed_outputs[arg]

    @classmethod
    def setUpClass(cls):
        testbed = """
        devices:
          R1:
            os: ios
            type: router
            connections: {}
        """
        cls.tb = Genie.init(testbed)
        cls.device = cls.tb.devices['R1']
        cls.device.parse = cls.get_parsed_output

    def test_verify_existing_file(self):
        exist = verify_file_exists(
            self.device,
            'bootflash:/packages.conf')
        self.assertEqual(exist, True)

    def test_verify_not_existing_file(self):
        exist = verify_file_exists(
            self.device,
            'bootflash:/some_file.zip')
        self.assertEqual(exist, False)

    def test_verify_not_existing_folder(self):
        self.device.parse = Mock(
            side_effect=SchemaEmptyParserError('error'))
        exist = verify_file_exists(
            self.device,
            'bootflash:/not_existing_folder/not_existing_file.zip')
        self.assertEqual(exist, False)

    def test_verify_not_existing_folder2(self):
        self.device.parse = Mock(
            side_effect=SchemaEmptyParserError('error'))
        exist = verify_file_exists(
            self.device,
            'flash:/some_file.zip')
        self.assertEqual(exist, False)


if __name__ == '__main__':
    unittest.main()
