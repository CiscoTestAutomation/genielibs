from unittest import TestCase
from genie.libs.sdk.apis.iosxe.stack.utils import free_up_disk_space
from unittest.mock import Mock


class TestFreeUpDiskSpace(TestCase):

    def test_free_up_disk_space(self):
        self.device = Mock()
        destination= 'bootflash'
        protect_files = ['image.bin']
        dir_parse ={'dir': {'dir': 'flash:/',
                         'flash:/': {'bytes_free': '494469120',
                                    'bytes_total': '11353194496',
                                    'files': {'PATCH': {
                                              'index': '442374',
                                              'last_modified_date': 'Sep 20 2025 '
                                                                '06:31:30 '
                                                                '+00:00',
                                                'size': '4096'}}}}}   
        self.device.api.get_available_space = Mock(return_value= 100)
        self.device.api.get_running_image = Mock(return_value=[])
        self.device.api.verify_enough_disk_space = Mock(side_effect=[False, True])
        self.device.api.delete_unprotected_files = Mock()
        self.device.parse = Mock(return_value=dir_parse)
        dir_out= 'out'
        
        free_up_disk_space(self.device, destination= destination, required_size=110,
                           skip_deletion=False, protected_files=protect_files,dir_output=dir_out)
        
        self.device.api.delete_unprotected_files.assert_called_with(
            directory='bootflash', protected={'image.bin'}, files_to_delete=['PATCH'], dir_output='out', 
            allow_failure=False, destination='bootflash')
        
        
