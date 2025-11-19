import unittest
import re
from unittest.mock import MagicMock, patch, PropertyMock

from pyats.easypy import runtime
from genie.libs.sdk.apis.iosxe.support.tech_support import collect_install_log

class TestCollectInstallLog(unittest.TestCase):

    @patch('genie.libs.sdk.apis.iosxe.support.tech_support.log')
    @patch('genie.libs.sdk.apis.iosxe.support.tech_support.get_default_dir')
    @patch('genie.libs.sdk.apis.iosxe.support.tech_support.datetime')
    def test_collect_install_log_telnet(self, mock_datetime, mock_get_default_dir, mock_log):
        mock_datetime.utcnow.return_value.strftime.return_value = "20250101T000000000"
        mock_get_default_dir.return_value = "flash:"
        with patch.object(type(runtime), 'directory', new_callable=PropertyMock) as mock_dir:
            mock_dir.return_value = "/tmp"
            device = MagicMock()
            device.connections = {'telnet': True}
            device.default_connection_alias = 'ssh'
            device.api.copy_from_device.return_value = True
            device.execute.side_effect = [
                None, # show platform software install-manager r0 operation current detail
                None, # show platform software install-manager r0 operation history detail
                None, # show tech-support install | append show_tech_support.txt
                "Done with creation of the archive file:[flash:archive.tar.gz]", # request platform software trace archive
                "Directory of flash:/" # dir
            ]

            with patch('re.search') as mock_search:
                mock_match = MagicMock()
                mock_match.group.return_value = "flash:archive.tar.gz"
                mock_search.return_value = mock_match
                collect_install_log(device)
                self.assertEqual(device.default_connection_alias, 'ssh')

                device.api.copy_from_device.assert_any_call(local_path="flash:show_tech_support_20250101T000000.txt", remote_path="/tmp")
                device.api.copy_from_device.assert_any_call(local_path="flash:archive.tar.gz", remote_path="/tmp")

    @patch('genie.libs.sdk.apis.iosxe.support.tech_support.log')
    def test_collect_install_log_no_telnet(self, mock_log):
        device = MagicMock()
        device.connections = {}
        device.execute.side_effect = [
            None, # show platform software install-manager r0 operation current detail
            None, # show platform software install-manager r0 operation history detail
            None, # show tech-support install | append show_tech_support.txt
            "Done with creation of the archive file:[flash:archive.tar.gz]", # request platform software trace archive
            "Directory of flash:/" # dir
        ]

        with patch('re.search') as mock_search:
            mock_match = MagicMock()
            mock_match.group.return_value = "flash:archive.tar.gz"
            mock_search.return_value = mock_match
            collect_install_log(device)
            mock_log.info.assert_any_call("Could not copy the install failure logs to runinfo directory")

if __name__ == '__main__':
    unittest.main()
