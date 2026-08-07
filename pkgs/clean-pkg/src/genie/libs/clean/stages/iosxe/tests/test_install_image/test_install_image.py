import unittest
import logging

from unittest.mock import Mock, MagicMock, patch
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.stages import InstallImage
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal

logger = logging.getLogger(__name__)

class TestInstallImage(unittest.TestCase):
    """ Run unit testing on a mocked IOSXE cat9k device """

    def setUp(self):
        self.cls = InstallImage()
        self.device = create_test_device('router', os='iosxe', platform='cat9k')
        self.device.state_machine = Mock()
        self.device.spawn = Mock()
        self.device.spawn.read_update_buffer = Mock(return_value='')
        self.device.spawn.match_buffer = Mock(return_value=False)

        self.device.api = Mock()
        self.device.api.get_platform_default_dir = Mock(return_value='bootflash:/')
        self.device.api.get_file_size_from_server = Mock(return_value=100000)
        self.device.api.verify_enough_disk_space = Mock(return_value=True)
        self.device.api.get_running_image = Mock(return_value='old_image.bin')
        self.device.api.copy_from_device = Mock(return_value=True)

        self.image = 'image.bin'

        # Mock the history attribute
        self.cls.history = {
            "InstallImage": type('MockParameters', (), {
                'parameters': {"image_mapping": {}}
            })()
        }

        self.data = {
            'show version | include operating mode': '',
            'show install summary': '',
            'show version': '''
                Cisco IOS XE Software, Version 17.12.01
                cisco C9300-24U (X86_64_LINUX_IOSXE) processor
            ''',
            'show install active': '''
                [ Switch 1 ] Active Package(s) Information:
                State (St): I - Inactive, U - Activated & Uncommitted,
                            C - Activated & Committed, D - Deactivated & Uncommitted
                --------------------------------------------------------------------------------
                Type  St   Filename/Version
                --------------------------------------------------------------------------------
                IMG   C    26.01.01.0.228502

                --------------------------------------------------------------------------------
                Auto abort timer: inactive
                --------------------------------------------------------------------------------
            ''',
            'install add file image.bin activate commit prompt-level none': '''
                install_add_activate_commit: START Sat Apr 11 20:33:55 UTC 2015
                install_add: START Sat Apr 11 20:33:55 UTC 2015
                install_add: Adding IMG
                  [1]  R0 FAILED: System configuration has been modified. Please save configuration and resubmit command.
                  [1]  R1 FAILED: Install ISSU in progress. Abort the ISSU upgrade to proceed
                FAILED: add_activate_commit image.bin Sat Apr 11 20:33:55 UTC 2015
            ''',
            'show issu state detail': '''
                Current ISSU Status: Enabled
                Previous ISSU Operation: Failed
                =======================================================
                System Check                        Status
                -------------------------------------------------------
                Platform ISSU Support               Yes
                Standby Online                      Yes
                Autoboot Enabled                    Yes
                SSO Mode                            Yes
                Install Boot                        Yes
                Valid Boot Media                    Yes
                Operational Mode                    HA-STANDALONE
                =======================================================
                No ISSU operation is in progress
            ''',
            'install abort issu': '''
                install_abort: START Sat Apr 11 20:34:13 UTC 2015
                FAILED: install_abort : System configuration has been modified. Please save configuration and resubmit command.
            ''',
            'copy running-config startup-config': '''
                Destination filename [startup-config]?
                Building configuration...
                [OK]
            ''',
            'write memory': '''
                Building configuration...
                [OK]
            ''',
            'show platform software install-manager r0 operation current detail': '',
            'show platform software install-manager r0 operation history detail': '',
            'request platform software trace archive': '''
                Done with creation of the archive file: [bootflash:archive.tar.gz]
            ''',
            'dir': '''
                Directory of bootflash:/
            ''',
            'install commit': '''
                install_commit: START
                install_commit: SUCCESS
            ''',
        }

    @patch('genie.libs.sdk.apis.iosxe.support.tech_support.datetime')
    def test_issu_in_progress(self, mock_datetime):
        mock_datetime.utcnow.return_value.strftime.return_value = '20250101T000000000'
        
        steps = Steps()

        self.device.execute = Mock(side_effect=lambda x, **y: self.data.get(x, ''))

        # Keep the unit test fast and deterministic by avoiding long dialog waits.
        self.cls.install_image(
            steps=steps,
            device=self.device,
            images=[self.image],
            reload_wait=1,
        )

        # Check the results is as expected.
        self.assertEqual(Passed, steps.details[0].result)

    @patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_empty_install_output_with_dialog_success_does_not_fail(self, dialog):
        steps = Steps()
        dialogs = []

        def _dialog(statements):
            mock_dialog = Mock()
            mock_dialog.statements = statements
            dialogs.append(mock_dialog)
            return mock_dialog

        dialog.side_effect = _dialog

        def _execute(cmd, **kwargs):
            if cmd == 'install add file image.bin activate commit prompt-level none':
                success_statement = next(
                    statement for statement in dialogs[0].statements
                    if 'SUCCESS:' in str(statement.pattern)
                    and getattr(statement, 'action', None)
                )
                success_statement.action(None, None)
                return ''
            return self.data.get(cmd, '')

        self.device.execute = Mock(side_effect=_execute)
        self.device.reload = Mock()

        self.cls.install_image(
            steps=steps,
            device=self.device,
            images=[self.image],
            reload_wait=1,
        )

        self.assertFalse(any(detail.result == Failed for detail in steps.details))
