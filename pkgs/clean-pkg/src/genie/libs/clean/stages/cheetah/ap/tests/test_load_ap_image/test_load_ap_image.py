import logging
import unittest
from unittest.mock import patch, Mock


from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.topology import loader


# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class TestLoadApImage(unittest.TestCase):

    def setUp(self):
        # Instantiate class object

        self.steps = Steps()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('AP4001.7AB2.C1B6', os='cheetah', platform='ap')
        self.device.testbed = loader.load({})
        self.device.testbed.servers = {
                "credentials": {
                    "default": {
                        "username": "username",
                        "password": "password"
                    }
                },
                "address": "1.1.1.1",
                "protocol": "tftp",
                "custom": {
                    "collection_upload_server": "tftp"
                }
            }
        self.device.api.execute_archive_download = Mock()

    @patch('pyats.utils.fileutils.FileUtils')
    def test_load_image(self, mock_file_utils):
        # need to import here because we are mocking the pyats.cli.utils.cmd function
        from genie.libs.clean.stages.cheetah.ap.stages import LoadApImage

        self.cls = LoadApImage()

        fu_instance = mock_file_utils.return_value
        fu_instance.get_auth.return_value = ('username', 'password')
        self.cls.load_image(self.device, self.steps, "/path/to/ap_image_path", self.device.testbed.servers)
        self.device.api.execute_archive_download.assert_called_once()