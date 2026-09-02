import hashlib
import unittest

from unittest.mock import Mock, call, mock_open, patch

from pyats.aetest.steps import Steps
from pyats.topology import Testbed

from genie.libs.clean.stages.stages import RecoveryImage
from genie.libs.clean.stages.tests.utils import create_test_device


class TestRecoveryImage(unittest.TestCase):

    def setUp(self):
        self.device = create_test_device('uut', os='iosxe')
        self.device.clean = {}
        self.device.execute = Mock(side_effect=['no golden image',
                                                 'golden_image.bin'])
        self.device.api.get_file_size_from_server = Mock(return_value=100)
        self.device.api.verify_file_exists = Mock(side_effect=[False, True])
        self.device.api.copy_to_device = Mock(return_value=True)
        self.device.api.lookup_default_image = Mock()
        self.device.api.get_platform_default_dir = Mock(
            return_value='bootflash:')

        self.file_utils = Mock()
        self.file_utils.get_server_block.return_value = {'path': '/images'}
        self.file_utils.get_hostname.return_value = '10.0.0.1'

    def test_exec_order(self):
        self.assertEqual(
            RecoveryImage.exec_order,
            [
                'resolve_recovery_image',
                'resolve_recovery_server',
                'check_golden_image',
                'copy_recovery_image',
                'verify_golden_image',
                'update_device_recovery',
            ])

    def test_protocol_default_ports(self):
        self.assertEqual(RecoveryImage._default_port('ftp'), 21)
        self.assertEqual(RecoveryImage._default_port('http'), 80)
        self.assertEqual(RecoveryImage._default_port('https'), 443)
        self.assertEqual(RecoveryImage._default_port('scp'), 22)
        self.assertEqual(RecoveryImage._default_port('sftp'), 22)
        self.assertEqual(RecoveryImage._default_port('tftp'), 69)
        self.assertIsNone(RecoveryImage._default_port('unknown'))

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_copies_source_to_stable_golden_image(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils

        RecoveryImage()(
            steps=Steps(),
            device=self.device,
            images=['/images/ir1101-build.bin'],
            golden_image=['bootflash:golden_image.bin'],
            recovery_server='recovery-server')

        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https',
            server='recovery-server',
            remote_path='/ir1101-build.bin',
            local_path='bootflash:golden_image.bin',
            vrf='',
            timeout=300,
            prompt_recovery=False)
        self.assertEqual(
            self.device.clean['device_recovery']['golden_image'],
            ['bootflash:golden_image.bin'])
        self.device.api.lookup_default_image.assert_not_called()
        file_utils_cls.from_device.assert_called_once_with(
            self.device, protocol='https')

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_uses_resolved_image_from_clean_data(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        self.device.clean = {
            'images': ['/images/utah-build.bin']
        }

        RecoveryImage()(
            steps=Steps(),
            device=self.device,
            golden_image=['bootflash:golden_image.bin'],
            recovery_server='recovery-server')

        self.device.api.lookup_default_image.assert_not_called()
        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https',
            server='recovery-server',
            remote_path='/utah-build.bin',
            local_path='bootflash:golden_image.bin',
            vrf='',
            timeout=300,
            prompt_recovery=False)

    def test_skips_without_recovery_inputs(self):
        # Normal clean images do not opt a device into recovery-image staging.
        # Shared templates may include this stage for devices whose LaaS
        # metadata has no recovery-image attributes.
        self.device.clean = {'images': ['/images/default-build.bin']}
        stage = RecoveryImage()
        stage.skipped = Mock(side_effect=RuntimeError)

        with self.assertRaises(RuntimeError):
            stage(steps=Steps(), device=self.device, verify_size=True)

        self.assertIn(
            'No recovery-image source or golden-image target was configured',
            stage.skipped.call_args.args[0])
        self.device.api.get_platform_default_dir.assert_not_called()
        self.device.api.get_file_size_from_server.assert_not_called()
        self.device.api.copy_to_device.assert_not_called()

    def test_does_not_resolve_image_metadata_at_stage_runtime(self):
        self.device.clean = {
            'images': [{
                'attributes': {
                    'recovery_image_branch': 'polaris_dev',
                    'recovery_image_build_target': 'utah_universalk9-image',
                }
            }]
        }
        self.device.execute = Mock(return_value='golden_image.bin')
        self.device.api.verify_file_exists = Mock(return_value=True)

        RecoveryImage()(steps=Steps(), device=self.device,
                        golden_image=['bootflash:golden_image.bin'])

        self.device.api.lookup_default_image.assert_not_called()

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_md5_is_authoritative_for_existing_target(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        server_device = Mock()
        server_device.api.get_md5_hash_of_file.return_value = 'abc123'
        self.device.api.convert_server_to_linux_device = Mock(
            return_value=server_device)
        self.device.api.get_md5_hash_of_file = Mock(return_value='bad-md5')
        self.device.execute = Mock(return_value='golden_image.bin')
        self.device.api.verify_file_exists = Mock(return_value=True)
        stage = RecoveryImage()
        stage.failed = Mock(side_effect=RuntimeError)

        with self.assertRaises(RuntimeError):
            stage(steps=Steps(), device=self.device,
                  images=['/images/recovery.bin'],
                  golden_image=['bootflash:golden_image.bin'],
                  recovery_server='recovery-server',
                  verify_md5=True)

        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https', server='recovery-server',
            remote_path='/recovery.bin',
            local_path='bootflash:golden_image.bin', vrf='', timeout=300,
            overwrite=True, prompt_recovery=False)

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_skips_matching_md5_target(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        server_device = Mock()
        server_device.api.get_md5_hash_of_file.return_value = 'abc123'
        self.device.api.convert_server_to_linux_device = Mock(
            return_value=server_device)
        self.device.api.get_md5_hash_of_file = Mock(return_value='abc123')
        self.device.execute = Mock(return_value='golden_image.bin')
        self.device.api.verify_file_exists = Mock(return_value=True)

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server', verify_md5=True)

        self.device.api.copy_to_device.assert_not_called()
        server_device.api.get_md5_hash_of_file.assert_called_once_with(
            '/images/recovery.bin', timeout=300)
        server_device.disconnect.assert_called_once_with()

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_uses_existing_device_recovery_target(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        self.device.clean = {
            'device_recovery': {
                'golden_image': ['bootflash:existing-golden.bin']
            }
        }

        RecoveryImage()(
            steps=Steps(),
            device=self.device,
            images=['/images/recovery.bin'],
            recovery_server='recovery-server')

        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https',
            server='recovery-server',
            remote_path='/recovery.bin',
            local_path='bootflash:existing-golden.bin',
            vrf='',
            timeout=300,
            prompt_recovery=False)

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_does_not_fetch_remote_metadata_before_copy(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        RecoveryImage()(
            steps=Steps(),
            device=self.device,
            images=['/images/ir1101-build.bin'],
            golden_image=['bootflash:golden_image.bin'],
            recovery_server='recovery-server')

        self.device.api.get_file_size_from_server.assert_not_called()
        self.device.api.copy_to_device.assert_called_once()

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_preserves_explicit_http_port_443(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server',
                        recovery_server_port=443,
                        protocol='http')

        self.device.api.get_file_size_from_server.assert_not_called()
        self.device.api.copy_to_device.assert_called_once_with(
            protocol='http', server='recovery-server',
            remote_path='/recovery.bin',
            local_path='bootflash:golden_image.bin', vrf='', timeout=300,
            prompt_recovery=False, port=443)

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_passes_non_default_https_port(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server',
                        recovery_server_port=8443)

        self.device.api.get_file_size_from_server.assert_not_called()
        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https', server='recovery-server',
            remote_path='/recovery.bin',
            local_path='bootflash:golden_image.bin', vrf='', timeout=300,
            prompt_recovery=False, port=8443)

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_verifies_existing_target_without_remote_source(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        self.device.clean = {'device_recovery': {
            'golden_image': ['bootflash:golden_image.bin']}}
        self.device.execute = Mock(return_value='golden_image.bin')
        self.device.api.verify_file_exists = Mock(return_value=True)

        RecoveryImage()(steps=Steps(), device=self.device)

        self.device.api.get_file_size_from_server.assert_not_called()
        self.device.api.copy_to_device.assert_not_called()
        self.assertEqual(
            self.device.clean['device_recovery']['golden_image'],
            ['bootflash:golden_image.bin'])

    def test_rejects_md5_verification_without_remote_source(self):
        self.device.clean = {'device_recovery': {
            'golden_image': ['bootflash:golden_image.bin']}}
        self.device.execute = Mock(return_value='golden_image.bin')
        self.device.api.verify_file_exists = Mock(return_value=True)
        self.device.api.get_md5_hash_of_file = Mock()
        stage = RecoveryImage()
        stage.failed = Mock(side_effect=RuntimeError)

        with self.assertRaises(RuntimeError):
            stage(steps=Steps(), device=self.device, verify_md5=True)

        self.assertIn('verify_md5 requires a remote recovery image source',
                      stage.failed.call_args.args[0])
        self.device.api.get_md5_hash_of_file.assert_not_called()

    def test_rejects_size_verification_without_remote_source(self):
        self.device.clean = {'device_recovery': {
            'golden_image': ['bootflash:golden_image.bin']}}
        self.device.execute = Mock(return_value='golden_image.bin')
        self.device.api.verify_file_exists = Mock(return_value=True)
        stage = RecoveryImage()
        stage.failed = Mock(side_effect=RuntimeError)

        with self.assertRaises(RuntimeError):
            stage(steps=Steps(), device=self.device, verify_size=True)

        self.assertIn('verify_size requires a remote recovery image source',
                      stage.failed.call_args.args[0])
        self.device.api.get_file_size_from_server.assert_not_called()

    @patch('genie.libs.clean.stages.stages.os.path.getsize',
           return_value=100)
    @patch('genie.libs.clean.stages.stages.os.path.isfile',
           return_value=True)
    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_skips_target_with_matching_size(
            self, file_utils_cls, isfile, getsize):
        file_utils_cls.from_device.return_value = self.file_utils
        self.device.execute = Mock(return_value='golden_image.bin')
        self.device.api.verify_file_exists = Mock(
            side_effect=[True, True, True, True])

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server',
                        verify_size=True)

        getsize.assert_called_once_with('/images/recovery.bin')
        self.device.api.get_file_size_from_server.assert_not_called()
        self.device.api.verify_file_exists.assert_has_calls([
            call(file='bootflash:/golden_image.bin', size=None,
                 dir_output='golden_image.bin'),
            call(file='bootflash:/golden_image.bin', size=100,
                 dir_output='golden_image.bin'),
        ])
        self.device.api.copy_to_device.assert_not_called()

    @patch('genie.libs.clean.stages.stages.os.path.getsize',
           return_value=100)
    @patch('genie.libs.clean.stages.stages.os.path.isfile',
           return_value=True)
    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_overwrites_target_with_different_size(
            self, file_utils_cls, isfile, getsize):
        file_utils_cls.from_device.return_value = self.file_utils
        self.device.execute = Mock(return_value='golden_image.bin')
        self.device.api.verify_file_exists = Mock(
            side_effect=[True, False, True, True])

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server',
                        verify_size=True)

        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https', server='recovery-server',
            remote_path='/recovery.bin',
            local_path='bootflash:golden_image.bin', vrf='', timeout=300,
            overwrite=True, prompt_recovery=False)

    @patch('genie.libs.clean.stages.stages.os.path.getsize',
           return_value=100)
    @patch('genie.libs.clean.stages.stages.os.path.isfile',
           return_value=True)
    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_fails_when_copied_target_has_wrong_size(
            self, file_utils_cls, isfile, getsize):
        file_utils_cls.from_device.return_value = self.file_utils
        self.device.api.verify_file_exists = Mock(
            side_effect=[False, True, False])
        stage = RecoveryImage()
        stage.failed = Mock(side_effect=RuntimeError)

        with self.assertRaises(RuntimeError):
            stage(steps=Steps(), device=self.device,
                  images=['/images/recovery.bin'],
                  golden_image=['bootflash:golden_image.bin'],
                  recovery_server='recovery-server',
                  verify_size=True)

        self.assertIn('size verification failed',
                      stage.failed.call_args.args[0])
        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https', server='recovery-server',
            remote_path='/recovery.bin',
            local_path='bootflash:golden_image.bin', vrf='', timeout=300,
            prompt_recovery=False)

    @patch('genie.libs.clean.stages.stages.os.path.isfile',
           return_value=False)
    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_gets_size_from_recovery_server_when_source_is_not_local(
            self, file_utils_cls, isfile):
        file_utils_cls.from_device.return_value = self.file_utils
        self.device.api.verify_file_exists = Mock(
            side_effect=[False, True, True])

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server',
                        verify_size=True)

        self.device.api.get_file_size_from_server.assert_called_once_with(
            server='10.0.0.1', path='/recovery.bin', protocol='https',
            timeout=300, fu_session=self.file_utils)

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_copies_multiple_recovery_images(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        self.device.execute = Mock(return_value='images')
        self.device.api.verify_file_exists = Mock(
            side_effect=[False, False, True, True])

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/one.bin', '/images/two.bin'],
                        copy_images=['/short/123/one.bin',
                                     '/short/456/two.bin'],
                        recovery_server='recovery-server')

        self.assertEqual(self.device.api.copy_to_device.call_count, 2)
        self.assertEqual(
            [call.kwargs['local_path'] for call in
             self.device.api.copy_to_device.call_args_list],
            ['bootflash:golden_image_1.bin',
             'bootflash:golden_image_2.bin'])
        self.assertEqual(
            [call.kwargs['remote_path'] for call in
             self.device.api.copy_to_device.call_args_list],
            ['/short/123/one.bin', '/short/456/two.bin'])

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_uses_platform_default_directory_for_implicit_target(
            self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        self.device.api.get_platform_default_dir.return_value = 'flash:'

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        recovery_server='recovery-server')

        self.device.api.get_platform_default_dir.assert_called_once_with()
        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https', server='recovery-server',
            remote_path='/recovery.bin',
            local_path='flash:golden_image.bin', vrf='', timeout=300,
            prompt_recovery=False)

    def test_rejects_mismatched_source_and_target_counts(self):
        stage = RecoveryImage()
        stage.failed = Mock(side_effect=RuntimeError)

        with self.assertRaises(RuntimeError):
            stage(steps=Steps(), device=self.device,
                  images=['/images/one.bin', '/images/two.bin'],
                  golden_image=['bootflash:golden_image.bin'])

        self.assertIn('must match', stage.failed.call_args.args[0])

    def test_rejects_mismatched_source_and_copy_counts(self):
        stage = RecoveryImage()
        stage.failed = Mock(side_effect=RuntimeError)

        with self.assertRaises(RuntimeError):
            stage(steps=Steps(), device=self.device,
                  images=['/images/one.bin', '/images/two.bin'],
                  copy_images=['/short/123/one.bin'],
                  golden_image=[
                      'bootflash:golden_image_1.bin',
                      'bootflash:golden_image_2.bin'])

        self.assertIn('copy_images paths (1) must match',
                      stage.failed.call_args.args[0])

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_skips_existing_target_without_md5(
            self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        self.device.execute = Mock(return_value='golden_image.bin')
        self.device.api.verify_file_exists = Mock(return_value=True)

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server')

        self.device.api.get_file_size_from_server.assert_not_called()
        self.device.api.verify_file_exists.assert_has_calls([
            call(file='bootflash:/golden_image.bin', size=None,
                 dir_output='golden_image.bin'),
            call(file='bootflash:/golden_image.bin', size=None,
                 dir_output='golden_image.bin'),
        ])
        self.device.api.copy_to_device.assert_not_called()

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_copies_missing_target_without_md5(
            self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server')

        self.device.api.copy_to_device.assert_called_once()

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_similar_filename_does_not_count_as_existing_target(
            self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        self.device.execute = Mock(
            side_effect=['golden_image.bin.old', 'golden_image.bin'])

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server')

        self.device.api.verify_file_exists.assert_has_calls([
            call(file='bootflash:/golden_image.bin', size=None,
                 dir_output='golden_image.bin.old'),
            call(file='bootflash:/golden_image.bin', size=None,
                 dir_output='golden_image.bin'),
        ])
        self.device.api.copy_to_device.assert_called_once()

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_normalizes_inspection_path_without_changing_copy_target(
            self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server')

        self.device.api.verify_file_exists.assert_called_with(
            file='bootflash:/golden_image.bin', size=None,
            dir_output='golden_image.bin')
        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https', server='recovery-server',
            remote_path='/recovery.bin',
            local_path='bootflash:golden_image.bin', vrf='', timeout=300,
            prompt_recovery=False)

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_does_not_use_internal_short_path_api(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        self.file_utils.get_server_block.return_value = {
            'path': '/images',
            'services': {
                'https': {
                    'application': 'short-path-cache',
                    'protocol': 'https',
                    'type': 'file_transfer',
                },
            },
        }
        self.device.api.get_short_path = Mock()

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server')

        self.device.api.get_short_path.assert_not_called()
        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https', server='recovery-server',
            remote_path='/recovery.bin',
            local_path='bootflash:golden_image.bin', vrf='', timeout=300,
            prompt_recovery=False)

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_uses_pre_resolved_copy_path_without_changing_md5_source(
            self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        self.file_utils.get_server_block.return_value = {
            'path': '/',
            'services': {
                'tftp': {
                    'application': 'short-path-cache',
                    'port': 69,
                    'protocol': 'tftp',
                    'type': 'file_transfer',
                },
            },
        }
        server_device = Mock()
        server_device.api.get_md5_hash_of_file.return_value = 'abc123'
        self.device.api.convert_server_to_linux_device = Mock(
            return_value=server_device)
        self.device.api.get_md5_hash_of_file = Mock(return_value='abc123')
        self.device.api.get_short_path = Mock()

        RecoveryImage()(
            steps=Steps(), device=self.device,
            images=['/auto/images/recovery.bin'],
            copy_images=['/short/1234/recovery.bin'],
            golden_image=['bootflash:golden_image.bin'],
            recovery_server='recovery-server', protocol='tftp',
            verify_md5=True)

        self.device.api.get_short_path.assert_not_called()
        server_device.api.get_md5_hash_of_file.assert_called_once_with(
            '/auto/images/recovery.bin', timeout=300)
        self.device.api.copy_to_device.assert_called_once_with(
            protocol='tftp', server='recovery-server',
            remote_path='/short/1234/recovery.bin',
            local_path='bootflash:golden_image.bin', vrf='', timeout=300,
            prompt_recovery=False)

    @patch('genie.libs.clean.stages.stages.os.path.getsize',
           return_value=100)
    @patch('genie.libs.clean.stages.stages.os.path.isfile',
           return_value=True)
    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_uses_original_source_size_with_pre_resolved_copy_path(
            self, file_utils_cls, isfile, getsize):
        file_utils_cls.from_device.return_value = self.file_utils
        self.file_utils.get_server_block.return_value = {
            'path': '/',
            'services': {
                'tftp': {
                    'application': 'short-path-cache',
                    'port': 69,
                    'protocol': 'tftp',
                    'type': 'file_transfer',
                },
            },
        }
        self.device.api.verify_file_exists = Mock(
            side_effect=[False, True, True])

        RecoveryImage()(
            steps=Steps(), device=self.device,
            images=['/auto/images/recovery.bin'],
            copy_images=['/short/1234/recovery.bin'],
            golden_image=['bootflash:golden_image.bin'],
            recovery_server='recovery-server', protocol='tftp',
            verify_size=True)

        getsize.assert_called_once_with('/auto/images/recovery.bin')
        self.device.api.get_file_size_from_server.assert_not_called()
        self.device.api.copy_to_device.assert_called_once_with(
            protocol='tftp', server='recovery-server',
            remote_path='/short/1234/recovery.bin',
            local_path='bootflash:golden_image.bin', vrf='', timeout=300,
            prompt_recovery=False)

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_uses_local_source_for_md5_without_ssh(
            self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        digest = hashlib.md5(b'recovery-image').hexdigest()
        self.device.api.get_md5_hash_of_file = Mock(return_value=digest)
        self.device.api.convert_server_to_linux_device = Mock()

        image_open = mock_open()
        image_open.return_value.read.side_effect = [
            b'recovery', b'-image', b'']
        with patch('genie.libs.clean.stages.stages.os.path.isfile',
                   return_value=True), patch('builtins.open', image_open):
            RecoveryImage()(steps=Steps(), device=self.device,
                            images=['/local/recovery.bin'],
                            golden_image=['bootflash:golden_image.bin'],
                            recovery_server='recovery-server',
                            verify_md5=True)

        self.device.api.convert_server_to_linux_device.assert_not_called()
        image_open.return_value.read.assert_has_calls([
            call(1024 * 1024), call(1024 * 1024), call(1024 * 1024)])

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_discovers_https_server_and_port(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        testbed = Testbed('testbed')
        testbed.servers = {
            'https-server': {
                'address': '10.0.0.9',
                'services': {
                    'https': {
                        'type': 'file_transfer',
                        'protocol': 'https',
                        'port': 8443,
                    }
                }
            }
        }
        self.device.testbed = testbed
        self.file_utils.get_server_block.return_value = (
            testbed.servers['https-server'])

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'])

        self.device.api.get_file_size_from_server.assert_not_called()
        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https', server='https-server',
            remote_path='/images/recovery.bin',
            local_path='bootflash:golden_image.bin', vrf='', timeout=300,
            prompt_recovery=False, port=8443)

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_discovers_ordered_server_with_string_order(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        testbed = Testbed('testbed')
        testbed.servers = {
            'unordered-server': {
                'address': '10.0.0.8',
                'services': {
                    'https': {
                        'type': 'file_transfer',
                        'protocol': 'https',
                    }
                },
            },
            'ordered-server': {
                'address': '10.0.0.9',
                'services': {
                    'https': {
                        'type': 'file_transfer',
                        'protocol': 'https',
                        'order': '10',
                    }
                },
            },
        }
        self.device.testbed = testbed
        self.file_utils.get_server_block.return_value = (
            testbed.servers['ordered-server'])

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'])

        self.file_utils.get_server_block.assert_called_once_with(
            'ordered-server')

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_uses_port_from_highest_priority_service(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        self.file_utils.get_server_block.return_value = {
            'address': '10.0.0.9',
            'path': '/images',
            'services': {
                'lower-priority': {
                    'type': 'file_transfer',
                    'protocol': 'https',
                    'order': 20,
                    'port': 8443,
                },
                'higher-priority': {
                    'type': 'file_transfer',
                    'protocol': 'https',
                    'order': 10,
                    'port': 9443,
                },
            },
        }

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server')

        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https', server='recovery-server',
            remote_path='/recovery.bin',
            local_path='bootflash:golden_image.bin', vrf='', timeout=300,
            prompt_recovery=False, port=9443)

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_does_not_discover_non_https_server(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        testbed = Testbed('testbed')
        testbed.servers = {
            'ordered-tftp': {
                'address': '10.0.0.9',
                'services': {
                    'tftp': {
                        'order': 1,
                        'type': 'file_transfer',
                        'protocol': 'tftp',
                    }
                }
            }
        }
        self.device.testbed = testbed
        stage = RecoveryImage()
        stage.failed = Mock(side_effect=RuntimeError)

        with self.assertRaises(RuntimeError):
            stage(steps=Steps(), device=self.device,
                  images=['/images/recovery.bin'],
                  golden_image=['bootflash:golden_image.bin'])

        self.assertIn('No HTTPS recovery server was found',
                      stage.failed.call_args.args[0])

    @patch('genie.libs.clean.stages.stages.FileUtils')
    def test_verifies_md5_without_remote_transfer_fetch(self, file_utils_cls):
        file_utils_cls.from_device.return_value = self.file_utils
        server_device = Mock()
        server_device.api.get_md5_hash_of_file.return_value = 'abc123'
        self.device.api.convert_server_to_linux_device = Mock(
            return_value=server_device)
        self.device.api.get_md5_hash_of_file = Mock(return_value='abc123')

        RecoveryImage()(steps=Steps(), device=self.device,
                        images=['/images/recovery.bin'],
                        golden_image=['bootflash:golden_image.bin'],
                        recovery_server='recovery-server',
                        verify_md5=True)

        server_device.api.get_md5_hash_of_file.assert_called_once_with(
            '/images/recovery.bin', timeout=300)
        self.device.api.get_file_size_from_server.assert_not_called()
        self.device.api.copy_to_device.assert_called_once_with(
            protocol='https', server='recovery-server',
            remote_path='/recovery.bin',
            local_path='bootflash:golden_image.bin', vrf='', timeout=300,
            prompt_recovery=False)
        self.device.api.get_md5_hash_of_file.assert_called_once_with(
            'bootflash:golden_image.bin', timeout=300)
