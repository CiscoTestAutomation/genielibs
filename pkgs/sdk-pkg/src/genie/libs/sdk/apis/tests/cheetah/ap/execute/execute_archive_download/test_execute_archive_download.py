import unittest
from genie.libs.sdk.apis.cheetah.ap.execute import execute_archive_download
from unittest.mock import Mock
from genie.libs.clean.stages.tests.utils import create_test_device


class TestPerformArchiveDownload(unittest.TestCase):

    def setUp(self):
        self.device = create_test_device(name='AP4001.7AB2.C1B6', os='cheetah', platform='ap')

    def test_perform_archive_download_success(self):
        data = ["""BOOT path-list:      part2""",
                """Download script called with args:[-l tftp://9.4.58.10/ftp/ewlc/ap3g3-k9w8-tar.master-cisco.202309230809 -m 0]
                 Starting download AP image tftp://9.4.58.10/ftp/ewlc/ap3g3-k9w8-tar.master-cisco.202309230809 ...
                 It may take a few minutes. If longer, please abort command, check network and try again.
                 ######################################################################## 100.0%
                 Upgrading ...
                 status 'upgrade.sh: Script called with args:[NO_UPGRADE]'
                 do NO_UPGRADE, part2 is active part
                 status 'upgrade.sh: Script called with args:[-c PREDOWNLOAD]'
                 do PREDOWNLOAD, part2 is active part
                 status 'upgrade.sh: Creating before-upgrade.log'
                 status 'upgrade.sh: Start doing upgrade arg1=PREDOWNLOAD arg2=,from_cli arg3= ...'
                 status 'upgrade.sh: Using image /tmp/cli_part.tar on barbados ...'
                 status 'Image signing verify success.'
                 status 'upgrade.sh: ***** part to upgrade is part1 *******'
                 status 'upgrade.sh: AP version1: part1 17.14.0.21, img 17.14.0.21'
                 status 'upgrade.sh: Extracting and verifying image in part1...'
                 status 'upgrade.sh: BOARD generic case execute'
                 status 'upgrade.sh: mount ubifs /dev/ubivol/part1 as /bootpart, status=0'
                 status 'upgrade.sh: Untar /tmp/cli_part.tar to /bootpart/part1...'
                 status 'upgrade.sh: Sync image to disk...'
                 status 'upgrade.sh: status 'Successfully verified image in part1.''
                 status 'upgrade.sh: AP version2: part1 17.14.0.21, img 17.14.0.21'
                 status 'upgrade.sh: AP backup version: 17.14.0.21'
                 status 'upgrade.sh: Finished upgrade task.'
                 status 'upgrade.sh: Cleanup for do_upgrade...'
                 status 'upgrade.sh: /tmp/upgrade_in_progress cleaned'
                 status 'upgrade.sh: Cleanup tmp files ...'
                 status 'upgrade.sh: Script called with args:[ACTIVATE]'
                 do ACTIVATE, part2 is active part
                 status 'upgrade.sh: mount ubifs /dev/ubivol/part1 as /bootpart, status=0'
                 status 'upgrade.sh: Verifying image signature in part1'
                 status 'upgrade.sh: status 'Successfully verified image in part1.''
                 status 'upgrade.sh: activate part1, set BOOT to part1'
                 status 'upgrade.sh: AP primary version after reload: 17.14.0.21'
                 status 'upgrade.sh: AP backup version after reload: 17.14.0.21'
                 Successfully setup AP image.
                 Image download completed.
                 Archive done.""", """"BOOT path-list:      part1"""]
        self.device.execute = Mock(side_effect=data)
        self.device.reload = Mock()
        self.device.connect = Mock()
        result = execute_archive_download(self.device,
                                          "tftp://9.4.58.10/ftp/ewlc/ap3g3-k9w8-tar.master-cisco.202309230809", 300)
        self.assertEqual(result, True)

    def test_perform_archive_download_failure(self):
        data = ["""BOOT path-list:      part1""",
                """Download script called with args:[-l tftp://9.4.58.10/ftp/ewlc/ap3g3-k9w8-tar.master-cisco.202309230809 -m 0]
                 Starting download AP image tftp://9.4.58.10/ftp/ewlc/ap3g3-k9w8-tar.master-cisco.202309230809 ...
                 It may take a few minutes. If longer, please abort command, check network and try again.
                 ######################################################################## 100.0%
                 Upgrading ...
                 status 'upgrade.sh: Script called with args:[NO_UPGRADE]'
                 do NO_UPGRADE, part2 is active part
                 status 'upgrade.sh: Script called with args:[-c PREDOWNLOAD]'
                 do PREDOWNLOAD, part2 is active part
                 status 'upgrade.sh: Creating before-upgrade.log'
                 status 'upgrade.sh: Start doing upgrade arg1=PREDOWNLOAD arg2=,from_cli arg3= ...'
                 status 'upgrade.sh: Using image /tmp/cli_part.tar on barbados ...'
                 status 'Image signing verify success.'
                 status 'upgrade.sh: ***** part to upgrade is part1 *******'
                 status 'upgrade.sh: AP version1: part1 17.14.0.21, img 17.14.0.21'
                 status 'upgrade.sh: Extracting and verifying image in part1...'
                 status 'upgrade.sh: BOARD generic case execute'
                 status 'upgrade.sh: mount ubifs /dev/ubivol/part1 as /bootpart, status=0'
                 status 'upgrade.sh: Untar /tmp/cli_part.tar to /bootpart/part1...'
                 status 'upgrade.sh: Sync image to disk...'
                 status 'upgrade.sh: status 'Successfully verified image in part1.''
                 status 'upgrade.sh: AP version2: part1 17.14.0.21, img 17.14.0.21'
                 status 'upgrade.sh: AP backup version: 17.14.0.21'
                 status 'upgrade.sh: Finished upgrade task.'
                 status 'upgrade.sh: Cleanup for do_upgrade...'
                 status 'upgrade.sh: /tmp/upgrade_in_progress cleaned'
                 status 'upgrade.sh: Cleanup tmp files ...'
                 status 'upgrade.sh: Script called with args:[ACTIVATE]'
                 do ACTIVATE, part2 is active part
                 status 'upgrade.sh: mount ubifs /dev/ubivol/part1 as /bootpart, status=0'
                 status 'upgrade.sh: Verifying image signature in part1'
                 status 'upgrade.sh: status 'Successfully verified image in part1.''
                 status 'upgrade.sh: activate part1, set BOOT to part1'
                 status 'upgrade.sh: AP primary version after reload: 17.14.0.21'
                 status 'upgrade.sh: AP backup version after reload: 17.14.0.21'
                 Successfully setup AP image.
                 Image download completed.
                 Archive done.""", """"BOOT path-list:      part1"""]
        self.device.execute = Mock(side_effect=data)
        self.device.reload = Mock()
        self.device.connect = Mock()
        result = execute_archive_download(self.device,
                                          "tftp://9.4.58.10/ftp/ewlc/ap3g3-k9w8-tar.master-cisco.202309230809", 300, reload=True, retries=0)
        self.assertEqual(result, False)

    def test_perform_archive_download_failure_2(self):
        data = ["""BOOT path-list:      part1""",
                """Download script called with args:[-l tftp://9.4.58.10/ftp/ewlc/ap3g3-k9w8-tar.master-cisco.202309230809 -m 0]
                 Starting download AP image tftp://9.4.58.10/ftp/ewlc/ap3g3-k9w8-tar.master-cisco.202309230809 ...
                 It may take a few minutes. If longer, please abort command, check network and try again.
                 ######################################################################## 100.0%     
                 Image download failed.""", """"BOOT path-list:      part1"""]
        self.device.execute = Mock(side_effect=data)
        self.device.reload = Mock()
        self.device.connect = Mock()
        result = execute_archive_download(self.device,
                                          "tftp://9.4.58.10/ftp/ewlc/ap3g3-k9w8-tar.master-cisco.202309230809", 300, reload=True, retries=0)
        self.assertEqual(result, False)

