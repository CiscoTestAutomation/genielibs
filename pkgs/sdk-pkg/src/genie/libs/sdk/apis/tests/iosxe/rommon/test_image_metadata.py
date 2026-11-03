import copy
import sys
import types
import unittest
from concurrent.futures import Future
from functools import partial
from threading import Event
from unittest.mock import Mock, call, patch

from pyats.aetest.steps import Steps
from pyats.aetest.signals import TerminateStepSignal
from pyats.utils.schemaengine import SchemaError
from unicon.core.errors import SubCommandFailure

from genie.libs.clean.stages.iosxe.stages import RommonBoot
from genie.libs.clean.exception import FailedToBootException
from genie.metaparser.util.schemaengine import Schema
from genie.libs.sdk.apis.iosxe.rommon.configure import configure_rommon_tftp, configure_rommon_tftp_ha
from genie.libs.sdk.apis.iosxe.rommon.get import get_recovery_details, get_tftp_boot_command
from genie.libs.sdk.apis.iosxe.rommon.utils import device_rommon_boot
from genie.libs.sdk.apis.iosxe.c8kv.rommon import utils as c8kv_rommon_utils
from genie.libs.sdk.apis.iosxe.cat9k.c9800.c9800_cl.rommon import (
    utils as c9800_cl_rommon_utils,
)
from genie.libs.sdk.apis.iosxe.cat9k.c9200.rommon.get import (
    get_recovery_details as get_c9200_recovery_details,
    get_tftp_boot_command as get_c9200_tftp_boot_command,
)


class TestRommonImageMetadata(unittest.TestCase):

    # Synthetic long path reproduces the metadata without internal build names.
    IMAGE = ('/auto/image-builds/release-build-20200101_000000/'
             'nested/platform-image/build/linkfarm/platform-image-iso/'
             'platform.release-build-20200101_000000.test-image.bin')

    def setUp(self):
        self.device = Mock()
        self.device.name = 'c9300'
        self.device.is_ha = False
        self.device.subconnections = None
        self.device.clean = {}
        self.device.management = {
            'address': {'ipv4': '192.0.2.2/24'}, 'gateway': {'ipv4': '192.0.2.1'},
        }
        self.device.testbed.servers = {'tftp': {'address': '192.0.2.10', 'protocol': 'tftp'}}
        self.device.state_machine.current_state = 'rommon'
        self.device.default.state_machine = self.device.state_machine
        self.device.default.context = {'image_to_boot': 'flash:/stale-golden.bin'}
        self.device.api.get_recovery_details.side_effect = partial(get_recovery_details, self.device)
        self.device.api.get_tftp_boot_command.side_effect = partial(get_tftp_boot_command, self.device)
        self.device.api.configure_rommon_tftp.side_effect = partial(configure_rommon_tftp, self.device)
        self.device.api.configure_rommon_tftp_ha.side_effect = partial(configure_rommon_tftp_ha, self.device)
        self.device.api.device_rommon_boot.side_effect = partial(device_rommon_boot, self.device)
        self.device.api.verify_ignore_startup_config.return_value = False
        self.variables = {'TFTP_FILE': 'flash:/stale-golden.bin'}
        self.boot_images = []

        def execute(command, **kwargs):
            if command == 'set':
                return '\r\n'.join(f'{key}={value}' for key, value in self.variables.items())
            key, value = command.split('=', 1)
            self.variables[key] = value

        self.device.execute.side_effect = execute
        self.device.default.execute.side_effect = execute

    def nested_metadata(self):
        return [{'image': {'file': [self.IMAGE]}}]

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_c8kv_grub_recovery_keeps_configured_golden_with_tftp_metadata(self, sleep):
        self.device.clean = {'device_recovery': {'golden_image': ['GOLDEN IMAGE']}}
        self.device.default.context['grub_boot_image'] = None
        self.device.api.device_rommon_boot.side_effect = partial(c8kv_rommon_utils.device_rommon_boot, self.device)
        boot_images = []

        def go_to(state, spawn, timeout, context, dialog):
            boot_images.append((context['grub_boot_image'], context['image_to_boot']))
            self.device.state_machine.current_state = 'disable'

        self.device.default.state_machine.go_to.side_effect = go_to
        for metadata in ([self.IMAGE], self.nested_metadata()):
            with self.subTest(metadata=metadata):
                self.device.state_machine.current_state = 'rommon'
                RommonBoot().rommon_boot(Steps(), self.device, image=metadata, tftp={'image': metadata})
        self.assertEqual(boot_images, [('GOLDEN IMAGE', 'GOLDEN IMAGE')] * 2)
        self.device.api.get_tftp_boot_command.assert_not_called()
        self.device.api.configure_rommon_tftp.assert_not_called()

    def test_c8kv_api_lookup_selects_grub_override(self):
        from genie.conf.base import Device

        device = Device('c8kv', os='iosxe', platform='c8kv', model='c8kv')
        self.assertIs(device.api.get_api('device_rommon_boot', device), c8kv_rommon_utils.device_rommon_boot)

    def test_c8kv_explicit_golden_and_boot_options_are_forwarded(self):
        self.device.clean = {'device_recovery': {'golden_image': ['DEFAULT GOLDEN']}}
        golden_image = ['CUSTOM GOLDEN']
        tftp_boot = {'image': self.nested_metadata()}
        cache = {}
        for error_pattern in (None, [], ['custom error']):
            with self.subTest(error_pattern=error_pattern), \
                    patch.object(c8kv_rommon_utils, 'xe_generic_rommon_boot') as boot:
                c8kv_rommon_utils.device_rommon_boot(
                    self.device, golden_image, tftp_boot, error_pattern, 'custom grub pattern', 300,
                    tftp_boot_state=cache)
                boot.assert_called_once_with(
                    self.device, golden_image=golden_image, tftp_boot=tftp_boot, error_pattern=error_pattern,
                    grub_activity_pattern='custom grub pattern', timeout=300, tftp_boot_state=cache)

    def test_c8kv_without_golden_preserves_generic_recovery(self):
        tftp_boot = {'image': self.nested_metadata()}
        cache = {}
        with patch.object(c8kv_rommon_utils, 'xe_generic_rommon_boot') as boot:
            c8kv_rommon_utils.device_rommon_boot(self.device, tftp_boot=tftp_boot, tftp_boot_state=cache)
        boot.assert_called_once_with(
            self.device, golden_image=[], tftp_boot=tftp_boot, error_pattern=[],
            grub_activity_pattern=None, timeout=None, tftp_boot_state=cache)
        self.assertIs(boot.call_args.kwargs['tftp_boot'], tftp_boot)
        self.assertIs(boot.call_args.kwargs['tftp_boot_state'], cache)

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_c9800_cl_grub_recovery_keeps_configured_golden_with_tftp_metadata(self, sleep):
        self.device.clean = {'device_recovery': {'golden_image': ['GOLDEN IMAGE']}}
        self.device.default.context['grub_boot_image'] = None
        self.device.api.device_rommon_boot.side_effect = partial(
            c9800_cl_rommon_utils.device_rommon_boot, self.device)
        boot_images = []

        def go_to(state, spawn, timeout, context, dialog):
            boot_images.append((context['grub_boot_image'], context['image_to_boot']))
            self.device.state_machine.current_state = 'disable'

        self.device.default.state_machine.go_to.side_effect = go_to
        for metadata in ([self.IMAGE], self.nested_metadata()):
            with self.subTest(metadata=metadata):
                self.device.state_machine.current_state = 'rommon'
                RommonBoot().rommon_boot(
                    Steps(), self.device, image=metadata,
                    tftp={'image': metadata})
        self.assertEqual(
            boot_images, [('GOLDEN IMAGE', 'GOLDEN IMAGE')] * 2)
        self.device.api.get_tftp_boot_command.assert_not_called()
        self.device.api.configure_rommon_tftp.assert_not_called()

    def test_stage_schema_accepts_normalizable_image_formats(self):
        for metadata in (self.IMAGE, [self.IMAGE], {'file': [self.IMAGE]}, self.nested_metadata()):
            with self.subTest(metadata=metadata):
                Schema(RommonBoot.schema).validate({'image': metadata})
                Schema(RommonBoot.schema).validate({'tftp': {'image': metadata}})

    def test_devx_62550_supported_shapes_reach_tftp_file_as_scalar(self):
        # The original selector returned the outer mapping instead of its path.
        for metadata in (self.IMAGE, [self.IMAGE], {'file': [self.IMAGE]},
                         {'image': {'file': [self.IMAGE]}}, self.nested_metadata()):
            with self.subTest(metadata=metadata):
                self.device.execute.reset_mock()
                command, selected = get_tftp_boot_command(self.device, {'tftp_boot': {'image': metadata}})
                self.assertEqual(command, 'tftp:')
                self.assertIsInstance(selected, str)
                self.assertEqual(selected, self.IMAGE)
                configure_rommon_tftp(self.device, image_path=selected)
                self.device.execute.assert_any_call(f'TFTP_FILE={self.IMAGE}')
                self.assertEqual(self.variables['TFTP_FILE'], self.IMAGE)

    def test_configure_normalizes_direct_metadata(self):
        configure_rommon_tftp(self.device, image_path=self.nested_metadata())
        self.assertEqual(self.variables['TFTP_FILE'], self.IMAGE)

    def test_cat9k_quiet_assignment_is_verified_by_environment_readback(self):
        self.device.platform = 'cat9k'
        for model in ('c9300', 'c9200'):
            with self.subTest(model=model):
                self.device.model = model
                self.device.execute.reset_mock()
                configure_rommon_tftp(self.device, image_path=self.nested_metadata())
                self.assertEqual(self.device.execute.call_args_list[-2:],
                                 [call(f'TFTP_FILE={self.IMAGE}'), call('set')])
                self.assertEqual(self.variables['TFTP_FILE'], self.IMAGE)

    def test_untested_rommon_path_does_not_receive_speculative_readback(self):
        self.device.platform = 'other-platform'
        self.device.model = 'c9300'
        configure_rommon_tftp(self.device, image_path=self.nested_metadata())
        self.assertNotIn(call('set'), self.device.execute.call_args_list)

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_cat9k_missing_or_stale_readback_stops_before_boot(self, sleep):
        self.device.platform = 'cat9k'
        self.device.model = 'c9300'
        for environment in (None, '', 'TFTP_FILE=\r\n', 'TFTP_FILE=flash:/stale-golden.bin\r\n',
                            f'TFTP_FILE={self.IMAGE}\r\nTFTP_FILE={self.IMAGE}\r\n',
                            'TFTP_FILE=/auto/wrong-image.bin\r\n',
                            "TFTP_FILE={'image': {'file': ['/auto/image.bin']}}\r\n"):
            with self.subTest(environment=environment):
                # Firmware returns no error but retains an unusable environment.
                self.device.execute.side_effect = lambda command, **kwargs: environment if command == 'set' else ''
                with self.assertRaisesRegex(SubCommandFailure, 'readback did not match selected image'):
                    device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()})
                self.device.default.state_machine.go_to.assert_not_called()
                self.device.default.spawn.sendline.assert_not_called()
                self.device.enable.assert_not_called()

    def test_ha_readback_uses_each_rp_and_rejects_stale_second_rp(self):
        self.device.platform = 'cat9k'
        self.device.model = 'c9300'
        self.device.is_ha = True
        connections = [Mock(alias='a'), Mock(alias='b')]
        self.device.subconnections = connections
        self.device.management['rommon'] = {
            f'rp{index}': {'address': {'ipv4': f'192.0.2.{index + 2}/24'},
                           'gateway': {'ipv4': '192.0.2.1'}}
            for index in range(2)
        }
        for con, path in zip(connections, (self.IMAGE, 'flash:/stale-golden.bin')):
            con.state_machine.current_state = 'rommon'
            con.execute.side_effect = lambda cmd, path=path: f'TFTP_FILE={path}\r\n' if cmd == 'set' else ''
        with self.assertRaisesRegex(SubCommandFailure, 'readback did not match selected image'):
            configure_rommon_tftp_ha(self.device, image_path=self.nested_metadata())
        for con in connections:
            self.assertEqual(con.execute.call_args_list[-2:], [call(f'TFTP_FILE={self.IMAGE}'), call('set')])
        self.device.execute.assert_not_called()

    def test_cat9k_readback_accepts_assignment_echo_before_query_prompt(self):
        self.device.platform = 'cat9k'
        self.device.model = 'c9300'
        for image in (self.IMAGE, '/auto/asset.bin'):
            raw = (f'TFTP_FILE={image}\r\nswitch: set\r\n'
                   f'ABNORMAL_RESET_COUNT=2\r\nTFTP_FILE={image}\r\n')
            for environment in (raw, raw.replace('set', '', 1)):
                with self.subTest(image=image, environment=environment):
                    # Real C9300 nested execute retains this echo. Unicon removes
                    # the first query-command occurrence, possibly in the echo.
                    self.device.execute.side_effect = lambda cmd: environment if cmd == 'set' else ''
                    configure_rommon_tftp(self.device, image_path=[{'image': {'file': [image]}}])
                    self.assertEqual(self.device.execute.call_args_list[-2:],
                                     [call(f'TFTP_FILE={image}'), call('set')])

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_assignment_echo_cannot_substitute_for_environment_readback(self, sleep):
        self.device.platform = 'cat9k'
        self.device.model = 'c9300'
        for query_prompt in ('switch: set', 'switch: '):
            for actual in ('', 'TFTP_FILE=flash:/stale-golden.bin\r\n',
                           f'TFTP_FILE={self.IMAGE}\r\nTFTP_FILE={self.IMAGE}\r\n'):
                with self.subTest(query_prompt=query_prompt, actual=actual):
                    environment = f'TFTP_FILE={self.IMAGE}\r\n{query_prompt}\r\n{actual}'
                    self.device.execute.side_effect = lambda cmd, **kwargs: environment if cmd == 'set' else ''
                    with self.assertRaisesRegex(SubCommandFailure, 'readback did not match selected image'):
                        device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()})
                    self.device.default.state_machine.go_to.assert_not_called()
                    self.device.default.spawn.sendline.assert_not_called()
                    self.device.enable.assert_not_called()

    def test_invalid_primary_images_fail_before_any_rommon_variables(self):
        for metadata in (None, [], {}, {'wrong_key': [self.IMAGE]}, [self.IMAGE, '/auto/other.bin'],
                         [{'image': {'file': [self.IMAGE, '/auto/other.bin']}}],
                         self.IMAGE + '\vboot flash:/stale-golden.bin',
                         self.IMAGE + '\t', self.IMAGE + '\x00', self.IMAGE + '\x1b[D',
                         ' ' + self.IMAGE, self.IMAGE + ' ',
                         [{'image': {'file': [self.IMAGE + '\u2028boot tftp:']}}]):
            with self.subTest(metadata=metadata):
                self.device.execute.reset_mock()
                with self.assertRaises(SubCommandFailure):
                    configure_rommon_tftp(self.device, image_path=metadata)
                self.device.execute.assert_not_called()
        with self.assertRaisesRegex(SchemaError, 'missing'):
            get_tftp_boot_command(self.device, {'tftp_boot': {}})

    def test_empty_override_does_not_fall_back_to_clean_image(self):
        with patch('genie.libs.sdk.apis.iosxe.rommon.configure.get_image_handler') as get_handler:
            get_handler.return_value.image = [self.IMAGE]
            with self.assertRaisesRegex(SubCommandFailure, 'empty'):
                configure_rommon_tftp(self.device, image_path=[])
            get_handler.assert_not_called()
        self.device.execute.assert_not_called()

    def test_ha_uses_same_normalized_path_for_each_rp(self):
        self.device.is_ha = True
        connections = [Mock(alias='a'), Mock(alias='b')]
        for con in connections:
            con.state_machine.current_state = 'rommon'
        self.device.subconnections = connections
        self.device.management['rommon'] = {
            f'rp{index}': {'address': {'ipv4': f'192.0.2.{index + 2}/24'},
                           'gateway': {'ipv4': '192.0.2.1'}}
            for index in range(2)
        }
        configure_rommon_tftp_ha(self.device, image_path=self.nested_metadata())
        for con in connections:
            con.execute.assert_any_call(f'TFTP_FILE={self.IMAGE}')
            con.execute.reset_mock()
        with self.assertRaisesRegex(SubCommandFailure, 'exactly one'):
            configure_rommon_tftp_ha(self.device, image_path=[self.IMAGE, '/auto/other.bin'])
        for con in connections:
            con.execute.assert_not_called()

    def test_boot_rejects_invalid_metadata_before_state_changes_or_boot(self):
        self.device.clean = {'device_recovery': {'golden_image': ['flash:/stale-golden.bin']}}
        for metadata in (None, [], {'wrong_key': [self.IMAGE]}, [self.IMAGE, '/auto/other.bin']):
            with self.subTest(metadata=metadata), self.assertRaises(SchemaError):
                device_rommon_boot(self.device, tftp_boot={'image': metadata})
        self.device.api.execute_set_config_register.assert_not_called()
        self.device.api.execute_rommon_reset.assert_not_called()
        self.device.execute.assert_not_called()
        self.device.default.state_machine.go_to.assert_not_called()

    def test_invalid_cached_transport_image_fails_before_configuration_or_boot(self):
        missing = object()
        for metadata in (missing, None, [], False, 1, [self.IMAGE, '/auto/other.bin'],
                         str({'image': {'file': [self.IMAGE]}}),
                         self.IMAGE + '\t', self.IMAGE + '\x00', self.IMAGE + '\x1b[D',
                         ' ' + self.IMAGE, self.IMAGE + ' ',
                         self.IMAGE + '\vboot flash:/stale-golden.bin'):
            configure = Mock()
            state = {'command': 'tftp:', 'image': metadata, 'configure': configure}
            if metadata is missing:
                state.pop('image')
            with self.subTest(metadata=metadata), self.assertRaises(SchemaError):
                device_rommon_boot(self.device, tftp_boot={'image': [self.IMAGE]}, tftp_boot_state=state)
            configure.assert_not_called()
            self.device.api.execute_set_config_register.assert_not_called()
            self.device.api.execute_rommon_reset.assert_not_called()
            self.device.api.configure_ignore_startup_config.assert_not_called()
            self.device.execute.assert_not_called()
            self.device.default.state_machine.go_to.assert_not_called()
            self.device.default.spawn.sendline.assert_not_called()

    def test_stage_reports_invalid_metadata_without_retrying_or_using_stale_image(self):
        self.device.clean = {'device_recovery': {'golden_image': ['flash:/stale-golden.bin']}}
        for metadata in (None, [], {'wrong_key': [self.IMAGE]}, [self.IMAGE, '/auto/other.bin']):
            with self.subTest(metadata=metadata):
                steps = Steps()
                with self.assertRaises(TerminateStepSignal):
                    RommonBoot().rommon_boot(steps, self.device, tftp={'image': metadata})
                self.assertIn('Invalid ROMMON boot image metadata', steps.details[0].result.reason)
        self.device.api.device_rommon_boot.assert_not_called()
        self.device.execute.assert_not_called()

    def test_explicit_tftp_without_image_does_not_boot_configured_golden(self):
        self.device.clean = {'device_recovery': {'golden_image': ['flash:/stale-golden.bin']}}
        with self.assertRaises(TerminateStepSignal):
            RommonBoot().rommon_boot(Steps(), self.device, tftp={'tftp_server': '192.0.2.10'})
        self.device.api.device_rommon_boot.assert_not_called()
        self.device.default.state_machine.go_to.assert_not_called()

    def test_empty_stage_image_does_not_boot_default_golden_image(self):
        self.device.clean = {'device_recovery': {'golden_image': ['flash:/stale-golden.bin']}}
        self.device.api.device_rommon_boot = Mock()
        for metadata in ([], {}, ''):
            with self.subTest(metadata=metadata), self.assertRaises(TerminateStepSignal):
                RommonBoot().rommon_boot(Steps(), self.device, image=metadata)
        self.device.api.device_rommon_boot.assert_not_called()
        self.device.execute.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_c9200_normalizes_before_constructing_boot_url(self, sleep):
        self.device.name = 'c9200'
        self.device.api.get_recovery_details.side_effect = partial(get_c9200_recovery_details, self.device)
        self.device.api.get_tftp_boot_command.side_effect = partial(get_c9200_tftp_boot_command, self.device)
        commands = []

        def go_to(*args, **kwargs):
            commands.append(kwargs['context']['image_to_boot'])
            self.device.state_machine.current_state = 'disable'

        self.device.default.state_machine.go_to.side_effect = go_to
        for metadata in (self.IMAGE, [self.IMAGE], {'file': [self.IMAGE]},
                         {'image': {'file': [self.IMAGE]}}, self.nested_metadata()):
            with self.subTest(metadata=metadata):
                self.device.state_machine.current_state = 'rommon'
                device_rommon_boot(self.device, tftp_boot={'image': metadata, 'tftp_server': '192.0.2.10'})
                self.assertEqual(commands[-1], f'tftp://192.0.2.10/{self.IMAGE}')
                self.assertEqual(self.variables['TFTP_FILE'], self.IMAGE)

    def test_c9200_and_48p_reject_ambiguity_before_building_url(self):
        from genie.libs.sdk.apis.iosxe.cat9k.c9200.c9200_48p.rommon.get import (
            get_tftp_boot_command as get_c9200_48p_tftp_boot_command,
        )

        recovery_info = {'tftp_boot': {'image': [self.IMAGE, '/auto/second.bin'],
                                       'tftp_server': '192.0.2.10'}}
        for selector in (get_c9200_tftp_boot_command, get_c9200_48p_tftp_boot_command):
            with self.subTest(selector=selector), self.assertRaisesRegex(SchemaError, 'exactly one'):
                selector(self.device, recovery_info)

        self.device.api.get_recovery_details.side_effect = partial(get_c9200_recovery_details, self.device)
        self.device.api.get_tftp_boot_command.side_effect = partial(get_c9200_tftp_boot_command, self.device)
        self.device.parse.return_value = {}
        self.device.clean = {'device_recovery': recovery_info}
        self.device.api.device_rommon_boot = Mock()
        with self.assertRaises(TerminateStepSignal):
            RommonBoot().rommon_boot(Steps(), self.device)
        self.device.api.device_rommon_boot.assert_not_called()
        self.device.execute.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_recovery_tftp_options_and_selected_image_survive_retries(self, sleep):
        self.device.name = 'c9200'
        self.device.api.get_recovery_details.side_effect = partial(get_c9200_recovery_details, self.device)
        self.device.api.get_tftp_boot_command.side_effect = partial(get_c9200_tftp_boot_command, self.device)
        self.device.parse.return_value = {}
        tftp = {'image': self.nested_metadata(), 'tftp_server': '198.51.100.10',
                'ip_address': ['192.0.2.2'], 'subnet_mask': '255.255.255.0', 'gateway': '192.0.2.1'}
        self.device.clean = {'device_recovery': {'tftp_boot': tftp}}
        self.device.testbed.servers = {}
        original = copy.deepcopy(tftp)
        commands = []

        def go_to(*args, **kwargs):
            commands.append(kwargs['context']['image_to_boot'])
            self.boot_images.append(self.variables['TFTP_FILE'])
            if len(commands) == 3:
                self.device.state_machine.current_state = 'disable'
            else:
                self.variables['TFTP_FILE'] = 'flash:/stale-golden.bin'

        self.device.default.state_machine.go_to.side_effect = go_to
        RommonBoot().rommon_boot(Steps(), self.device, timeout=1, tftp_boot_sleep_interval=0)
        self.assertEqual(commands, [f'tftp://198.51.100.10/{self.IMAGE}'] * 3)
        self.assertEqual(self.boot_images, [self.IMAGE] * 3)
        expected = {**original, 'image': [self.IMAGE]}
        for args, kwargs in self.device.api.device_rommon_boot.call_args_list:
            self.assertEqual(kwargs['tftp_boot'], expected)
        self.assertEqual(tftp, original)

    def test_older_clean_fails_actionably_before_tftp_boot(self):
        # Missing normalization must fail before configuring or booting ROMMON.
        module_name = 'genie.libs.clean.stages.image_handler'
        older_clean = types.ModuleType(module_name)
        with patch.dict(sys.modules, {module_name: older_clean}):
            with self.assertRaisesRegex(ImportError, 'matching.*DEVX-62550'):
                device_rommon_boot(self.device, tftp_boot={'image': [self.IMAGE]})
            with self.assertRaisesRegex(SubCommandFailure, 'matching.*DEVX-62550') as error:
                configure_rommon_tftp(self.device, image_path=self.IMAGE)
            self.assertIsInstance(error.exception.__cause__, ImportError)
        self.device.api.execute_set_config_register.assert_not_called()
        self.device.execute.assert_not_called()
        self.device.default.state_machine.go_to.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_legacy_platform_selector_receives_canonical_paths(self, sleep):
        # Older/plugin selectors require a flat list and choose its first item.
        # Exercise both direct SDK boot and the stage's recovery preflight.
        def legacy_selector(recovery_info):
            image = recovery_info['tftp_boot']['image'][0]
            return f'tftp://192.0.2.10/{image}', image

        self.device.api.get_tftp_boot_command.side_effect = legacy_selector
        self.device.default.state_machine.go_to.side_effect = lambda *a, **k: setattr(
            self.device.state_machine, 'current_state', 'disable')
        for metadata in (self.IMAGE, [self.IMAGE], self.nested_metadata()):
            with self.subTest(metadata=metadata):
                self.device.state_machine.current_state = 'rommon'
                device_rommon_boot(self.device, tftp_boot={'image': metadata})
                self.assertEqual(self.variables['TFTP_FILE'], self.IMAGE)
                self.device.state_machine.current_state = 'rommon'
                self.device.clean = {'device_recovery': {'tftp_boot': {'image': metadata}}}
                original = copy.deepcopy(self.device.clean)
                RommonBoot().rommon_boot(Steps(), self.device, timeout=1)
                self.assertEqual(self.variables['TFTP_FILE'], self.IMAGE)
                self.assertEqual(self.device.clean, original)
        for args, kwargs in self.device.api.get_tftp_boot_command.call_args_list:
            self.assertEqual(args[0]['tftp_boot']['image'], [self.IMAGE])
            self.assertEqual(args[0]['tftp_image'], [self.IMAGE])

    def test_invalid_recovery_image_fails_before_platform_selector_dispatch(self):
        self.device.api.get_tftp_boot_command.side_effect = None
        for metadata in ([], {}, {'path': self.IMAGE}, [self.IMAGE, '/auto/second.bin']):
            with self.subTest(metadata=metadata):
                self.device.clean = {'device_recovery': {'tftp_boot': {'image': metadata}}}
                with self.assertRaises(SchemaError):
                    device_rommon_boot(self.device)
                with self.assertRaises(TerminateStepSignal):
                    RommonBoot().rommon_boot(Steps(), self.device)
        self.device.api.get_tftp_boot_command.assert_not_called()
        self.device.execute.assert_not_called()
        self.device.default.state_machine.go_to.assert_not_called()

    def test_real_platform_api_lookup_returns_normalized_paths(self):
        from genie.conf.base import api as api_module
        from genie.testbed import load

        # Test this repository's API abstraction without installed Cisco
        # extension overrides masking the changed C9200 implementation.
        with patch.object(api_module, 'get_entry_points', return_value=[]), \
                patch.object(api_module, 'function_data', None):
            for model, submodel in (('c9300', None), ('c9200', None), ('c9200', 'c9200-48p')):
                tokens = {'os': 'iosxe', 'platform': 'cat9k', 'model': model, 'connections': {}}
                if submodel:
                    tokens['submodel'] = submodel
                device = load({'devices': {'uut': tokens}}).devices['uut']
                device.clean = {}
                with self.subTest(model=model, submodel=submodel):
                    command, image = device.api.get_tftp_boot_command({
                        'tftp_boot': {'image': self.nested_metadata(), 'tftp_server': '192.0.2.10'}})
                    expected = 'tftp:' if model == 'c9300' else f'tftp://192.0.2.10/{self.IMAGE}'
                    self.assertEqual((command, image), (expected, self.IMAGE))

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_rommon_retry_path_reuses_selected_image_on_all_three_attempts(self, sleep):
        # Run real stage -> recovery getter -> ROMMON selector/configuration ->
        # boot dialog. Only device I/O and sleeps are mocked.
        self.device.clean = {'device_recovery': {'golden_image': ['flash:/stale-golden.bin']}}
        metadata = self.nested_metadata()
        original = copy.deepcopy(metadata)
        self.device.default.spawn.settings.MAX_BOOT_ATTEMPTS = 3

        def go_to(*args, **kwargs):
            self.boot_images.append(self.variables['TFTP_FILE'])
            statement = next(stmt for stmt in kwargs['dialog']
                             if getattr(stmt.action, '__name__', '') == '_rommon_switch_boot')
            statement.action(self.device.default.spawn, {}, kwargs['context'])
            if len(self.boot_images) == 3:
                self.device.state_machine.current_state = 'disable'
            else:
                # Simulate firmware reverting its variables after a failed boot.
                self.variables['TFTP_FILE'] = 'flash:/stale-golden.bin'

        self.device.default.state_machine.go_to.side_effect = go_to
        RommonBoot().rommon_boot(Steps(), self.device, tftp={'image': metadata},
                                 timeout=1, tftp_boot_sleep_interval=0)

        self.assertEqual(self.boot_images, [self.IMAGE] * 3)
        self.assertEqual(self.device.api.device_rommon_boot.call_count, 3)
        self.assertEqual(metadata, original)
        self.assertEqual(self.device.default.spawn.sendline.call_args_list, [call('boot tftp:')] * 3)
        file_commands = [args[0] for args, _ in self.device.execute.call_args_list
                         if args[0].startswith('TFTP_FILE=')]
        self.assertEqual(file_commands, [f'TFTP_FILE={self.IMAGE}'] * 3)
        for args, kwargs in self.device.api.configure_rommon_tftp.call_args_list:
            self.assertEqual(kwargs['image_path'], self.IMAGE)

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_provider_translation_is_frozen_for_inner_and_outer_retries(self, sleep):
        self.device.platform = 'cat9k'
        self.device.model = 'c9300'
        # Even an alias longer than 90 chars must not be shortened again.
        transport_image = '/short/provider-selected/' + 'x' * 100 + '.bin'
        self.device.api.get_short_path.return_value = transport_image

        def provider(**kwargs):
            # The installed legacy provider translates, delegates, and returns None.
            image = kwargs['image_path']
            if len(image) > 90:
                image = self.device.api.get_short_path(image)
            configure_rommon_tftp(self.device, image_path=image)

        self.device.api.configure_rommon_tftp.side_effect = provider
        self.device.default.spawn.settings.MAX_BOOT_ATTEMPTS = 3
        attempts = []
        outer_attempts = []

        def go_to(*args, **kwargs):
            attempts.append(self.variables['TFTP_FILE'])
            outer_attempts.append(self.variables['TFTP_FILE'])
            action = next(stmt.action for stmt in kwargs['dialog']
                          if getattr(stmt.action, '__name__', '') == '_rommon_switch_boot')
            self.device.default.spawn.sendline.side_effect = lambda command: attempts.append(
                self.variables['TFTP_FILE'])
            session = {}
            for _ in range(2):
                self.variables['TFTP_FILE'] = 'flash:/stale-golden.bin'
                action(self.device.default.spawn, session, kwargs['context'])
            if len(outer_attempts) == 3:
                self.device.state_machine.current_state = 'disable'
            else:
                self.variables['TFTP_FILE'] = 'flash:/stale-golden.bin'

        metadata = self.nested_metadata()
        original = copy.deepcopy(metadata)
        self.device.default.state_machine.go_to.side_effect = go_to
        RommonBoot().rommon_boot(Steps(), self.device, tftp={'image': metadata},
                                 timeout=1, tftp_boot_sleep_interval=0)
        self.device.api.get_short_path.assert_called_once_with(self.IMAGE)
        self.device.api.configure_rommon_tftp.assert_called_once_with(image_path=self.IMAGE)
        self.assertEqual(outer_attempts, [transport_image] * 3)
        self.assertEqual(attempts, [transport_image] * 9)
        self.assertEqual(metadata, original)
        for connection in (self.device, self.device.default):
            assignments = [args[0] for args, _ in connection.execute.call_args_list
                           if args[0].startswith('TFTP_FILE=')]
            self.assertEqual(assignments, [f'TFTP_FILE={transport_image}'] * (3 if connection is self.device else 6))

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_ha_provider_transport_is_reused_on_every_console_and_retry(self, sleep):
        self.device.platform = 'cat9k'
        self.device.model = 'c9300'
        self.device.is_ha = True
        connections = [Mock(alias='a'), Mock(alias='b')]
        self.device.subconnections = connections
        self.device.management['rommon'] = {
            f'rp{index}': {'address': {'ipv4': f'192.0.2.{index + 2}/24'},
                           'gateway': {'ipv4': '192.0.2.1'}}
            for index in range(2)
        }
        transport = '/short/provider-selected/image.bin'
        self.device.api.get_short_path.return_value = transport
        images = [[] for _ in connections]
        variables = [{'TFTP_FILE': 'flash:/stale-golden.bin'} for _ in connections]

        def provider(**kwargs):
            image = self.device.api.get_short_path(kwargs['image_path'])
            configure_rommon_tftp_ha(self.device, image_path=image)

        self.device.api.configure_rommon_tftp_ha.side_effect = provider
        for index, con in enumerate(connections):
            con.context = {'image_to_boot': 'flash:/stale-golden.bin'}
            con.spawn.settings.MAX_BOOT_ATTEMPTS = 3

            def execute(command, index=index, **kwargs):
                if command == 'set':
                    return f"TFTP_FILE={variables[index]['TFTP_FILE']}"
                key, value = command.split('=', 1)
                variables[index][key] = value

            def go_to(*args, index=index, **kwargs):
                con = connections[index]
                images[index].append(variables[index]['TFTP_FILE'])
                action = next(stmt.action for stmt in kwargs['dialog']
                              if getattr(stmt.action, '__name__', '') == '_rommon_switch_boot')
                variables[index]['TFTP_FILE'] = 'flash:/stale-golden.bin'
                con.spawn.sendline.side_effect = lambda command: images[index].append(variables[index]['TFTP_FILE'])
                action(con.spawn, {}, kwargs['context'])
                con.state_machine.current_state = 'disable'

            con.execute.side_effect = execute
            con.state_machine.go_to.side_effect = go_to
        state = {}
        for _ in range(2):
            for con, environment in zip(connections, variables):
                con.state_machine.current_state = 'rommon'
                environment['TFTP_FILE'] = 'flash:/stale-golden.bin'
            device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()},
                               timeout=1, tftp_boot_state=state)
        self.device.api.get_short_path.assert_called_once_with(self.IMAGE)
        self.device.api.configure_rommon_tftp_ha.assert_called_once_with(image_path=self.IMAGE)
        self.assertEqual(images, [[transport] * 4, [transport] * 4])
        self.assertEqual(state['image'], transport)
        self.assertEqual(self.device.connection_provider.designate_handles.call_count, 2)

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_provider_capture_is_scoped_and_failed_readback_is_not_cached(self, sleep):
        from genie.libs.sdk.apis.iosxe.rommon.configure import _rommon_tftp_image_capture

        self.device.platform = 'cat9k'
        self.device.model = 'c9300'
        state = {}
        self.device.execute.side_effect = lambda command, **kwargs: 'TFTP_FILE=flash:/stale-golden.bin'
        with self.assertRaisesRegex(SubCommandFailure, 'readback did not match'):
            device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()}, tftp_boot_state=state)
        self.assertEqual(state, {})
        self.assertIsNone(_rommon_tftp_image_capture.get())
        self.device.default.state_machine.go_to.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_provider_without_successful_delegation_cannot_boot_stale_image(self, sleep):
        self.device.api.configure_rommon_tftp.side_effect = None
        with self.assertRaisesRegex(SubCommandFailure, 'did not expose one successfully configured transport image'):
            device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()})
        self.device.default.state_machine.go_to.assert_not_called()
        self.device.default.spawn.sendline.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_failed_tftp_file_set_aborts_without_booting_or_retrying(self, sleep):
        def execute(command):
            if command.startswith('TFTP_FILE='):
                raise SubCommandFailure('ROMMON rejected TFTP_FILE')

        self.device.execute.side_effect = execute
        with self.assertRaises(TerminateStepSignal):
            RommonBoot().rommon_boot(Steps(), self.device, tftp={'image': self.nested_metadata()})
        self.device.api.device_rommon_boot.assert_called_once()
        self.device.execute.assert_any_call(f'TFTP_FILE={self.IMAGE}')
        self.device.default.state_machine.go_to.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_execute_usage_error_aborts_without_stale_boot_or_retry(self, sleep):
        # The execute service detects usage errors; Clean must stop before boot.
        for response in ('usage:\r\n\tset <variable-name>[OPTIONAL] <value>[OPTIONAL]\r\n',
                         'Usage: set <variable-name> <value>\n'):
            with self.subTest(response=response):
                self.device.api.device_rommon_boot.reset_mock()
                self.device.default.state_machine.go_to.reset_mock()

                def execute(command):
                    if command.startswith('TFTP_FILE='):
                        raise SubCommandFailure(response)
                    key, value = command.split('=', 1)
                    self.variables[key] = value

                self.device.execute.side_effect = execute
                steps = Steps()
                with self.assertRaises(TerminateStepSignal):
                    RommonBoot().rommon_boot(steps, self.device,
                                             tftp={'image': self.nested_metadata()})
                self.assertIn('Failed to set the rommon variable TFTP_FILE', steps.details[0].result.reason)
                self.assertIn(response, steps.details[0].result.reason)
                self.assertEqual(self.variables['TFTP_FILE'], 'flash:/stale-golden.bin')
                self.device.api.device_rommon_boot.assert_called_once()
                self.device.default.state_machine.go_to.assert_not_called()
                self.device.default.spawn.sendline.assert_not_called()

    def test_ha_execute_usage_error_aborts_before_configuring_next_rp(self):
        self.device.is_ha = True
        connections = [Mock(alias='a'), Mock(alias='b')]
        for con in connections:
            con.state_machine.current_state = 'rommon'
        def execute(command):
            if command.startswith('TFTP_FILE='):
                raise SubCommandFailure('usage:\r\n\tset <variable-name>[OPTIONAL] <value>[OPTIONAL]\r\n')

        connections[0].execute.side_effect = execute
        self.device.subconnections = connections
        self.device.management['rommon'] = {
            f'rp{index}': {'address': {'ipv4': f'192.0.2.{index + 2}/24'},
                           'gateway': {'ipv4': '192.0.2.1'}}
            for index in range(2)
        }
        with self.assertRaisesRegex(SubCommandFailure, 'usage:'):
            configure_rommon_tftp_ha(self.device, image_path=self.nested_metadata())
        connections[0].execute.assert_any_call(f'TFTP_FILE={self.IMAGE}')
        connections[1].execute.assert_not_called()

    @patch('genie.libs.clean.stages.iosxe.stages.time.sleep')
    def test_retry_arguments_remain_selected_even_if_api_mutates_them(self, sleep):
        images = []

        def boot(**kwargs):
            images.extend(kwargs['tftp_boot']['image'])
            kwargs['tftp_boot']['image'][0] = 'flash:/stale-golden.bin'
            if len(images) < 3:
                raise FailedToBootException('TFTP timeout')

        self.device.api.device_rommon_boot.side_effect = boot
        RommonBoot().rommon_boot(Steps(), self.device, image=self.nested_metadata(),
                                 tftp_boot_sleep_interval=0)
        self.assertEqual(images, [self.IMAGE] * 3)

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_recovery_config_image_is_normalized_and_selected_once(self, sleep):
        self.device.clean = {'device_recovery': {'tftp_boot': {'image': self.nested_metadata()}}}
        self.device.default.state_machine.go_to.side_effect = lambda *a, **k: setattr(
            self.device.state_machine, 'current_state', 'disable')
        RommonBoot().rommon_boot(Steps(), self.device, timeout=1)
        self.device.api.device_rommon_boot.assert_called_once()
        self.assertEqual(self.variables['TFTP_FILE'], self.IMAGE)
        self.assertEqual(self.device.api.device_rommon_boot.call_args.kwargs['tftp_boot']['image'], [self.IMAGE])

    def test_platform_validated_global_image_keeps_package_roles(self):
        from genie.libs.clean.stages.tests.utils import create_test_device

        device = create_test_device('c9300', 'iosxe')
        device.clean = {'images': {'image': {'file': [self.IMAGE]},
                                   'packages': {'file': ['/auto/pkg1.bin', '/auto/pkg2.bin']}}}
        recovery_info = get_recovery_details(device)
        self.assertEqual(get_tftp_boot_command(device, recovery_info), ('tftp:', self.IMAGE))

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_explicit_golden_image_precedence_is_preserved(self, sleep):
        images = []

        def go_to(*args, **kwargs):
            images.append(kwargs['context']['image_to_boot'])
            self.device.state_machine.current_state = 'disable'

        self.device.default.state_machine.go_to.side_effect = go_to
        device_rommon_boot(self.device, golden_image=['flash:/chosen-golden.bin'],
                           tftp_boot={'image': self.nested_metadata()})
        self.assertEqual(images, ['flash:/chosen-golden.bin'])
        self.device.api.get_tftp_boot_command.assert_not_called()
        self.device.execute.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_inner_rommon_retries_reapply_selected_image(self, sleep):
        self.device.platform = 'cat9k'
        self.device.model = 'c9300'
        conn = self.device.default
        conn.spawn.settings.MAX_BOOT_ATTEMPTS = 3

        def go_to(*args, **kwargs):
            action = next(stmt.action for stmt in kwargs['dialog']
                          if getattr(stmt.action, '__name__', '') == '_rommon_switch_boot')
            session = {}
            conn.spawn.sendline.side_effect = lambda cmd: self.boot_images.append(self.variables['TFTP_FILE'])
            for _ in range(3):
                self.variables['TFTP_FILE'] = 'flash:/stale-golden.bin'
                action(conn.spawn, session, kwargs['context'])
            with self.assertRaisesRegex(Exception, 'Too many failed boot attempts'):
                action(conn.spawn, session, kwargs['context'])
            self.device.state_machine.current_state = 'disable'

        conn.state_machine.go_to.side_effect = go_to
        device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()}, timeout=1)
        self.assertEqual(self.boot_images, [self.IMAGE] * 3)
        self.assertEqual(conn.execute.call_args_list, [call(f'TFTP_FILE={self.IMAGE}', timeout=1), call('set')] * 3)
        self.assertEqual(conn.spawn.sendline.call_args_list, [call('boot tftp:')] * 3)
        self.assertEqual(conn.context['image_to_boot'], 'flash:/stale-golden.bin')

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_inner_retry_set_rejection_stops_before_boot(self, sleep):
        conn = self.device.default
        conn.spawn.settings.MAX_BOOT_ATTEMPTS = 3
        conn.execute.side_effect = SubCommandFailure('Usage: set <variable-name> <value>\n')

        def go_to(*args, **kwargs):
            action = next(stmt.action for stmt in kwargs['dialog']
                          if getattr(stmt.action, '__name__', '') == '_rommon_switch_boot')
            self.variables['TFTP_FILE'] = 'flash:/stale-golden.bin'
            action(conn.spawn, {}, kwargs['context'])

        conn.state_machine.go_to.side_effect = go_to
        with self.assertRaisesRegex(SubCommandFailure, 'Usage: set'):
            device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()}, timeout=1)
        conn.spawn.sendline.assert_not_called()
        self.device.enable.assert_not_called()
        self.assertEqual(self.variables['TFTP_FILE'], 'flash:/stale-golden.bin')
        self.assertEqual(conn.context['image_to_boot'], 'flash:/stale-golden.bin')

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_inner_retry_returned_usage_stops_before_readback_or_boot(self, sleep):
        conn = self.device.default
        conn.spawn.settings.MAX_BOOT_ATTEMPTS = 3
        conn.execute.side_effect = lambda cmd, **kwargs: '\r\nswitch: usage: set NAME VALUE\r\n'

        def go_to(*args, **kwargs):
            action = next(stmt.action for stmt in kwargs['dialog']
                          if getattr(stmt.action, '__name__', '') == '_rommon_switch_boot')
            self.variables['TFTP_FILE'] = 'flash:/stale-golden.bin'
            action(conn.spawn, {}, kwargs['context'])

        conn.state_machine.go_to.side_effect = go_to
        with self.assertRaisesRegex(SubCommandFailure, '(?i)usage: set'):
            device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()}, timeout=1)
        conn.execute.assert_called_once_with(f'TFTP_FILE={self.IMAGE}', timeout=1)
        conn.spawn.sendline.assert_not_called()
        self.device.enable.assert_not_called()
        self.assertEqual(self.variables['TFTP_FILE'], 'flash:/stale-golden.bin')
        self.assertEqual(conn.context['image_to_boot'], 'flash:/stale-golden.bin')

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_inner_retry_silent_assignment_failure_stops_before_boot(self, sleep):
        self.device.platform = 'cat9k'
        self.device.model = 'c9200'
        conn = self.device.default
        conn.spawn.settings.MAX_BOOT_ATTEMPTS = 3
        conn.execute.side_effect = lambda cmd, **kwargs: (
            f"TFTP_FILE={self.variables['TFTP_FILE']}" if cmd == 'set' else '')

        def go_to(*args, **kwargs):
            action = next(stmt.action for stmt in kwargs['dialog']
                          if getattr(stmt.action, '__name__', '') == '_rommon_switch_boot')
            self.variables['TFTP_FILE'] = 'flash:/stale-golden.bin'
            action(conn.spawn, {}, kwargs['context'])

        conn.state_machine.go_to.side_effect = go_to
        with self.assertRaisesRegex(SubCommandFailure, 'readback did not match selected image'):
            device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()}, timeout=1)
        self.assertEqual(conn.execute.call_args_list, [call(f'TFTP_FILE={self.IMAGE}', timeout=1), call('set')])
        conn.spawn.sendline.assert_not_called()
        self.device.enable.assert_not_called()
        self.assertEqual(self.variables['TFTP_FILE'], 'flash:/stale-golden.bin')
        self.assertEqual(conn.context['image_to_boot'], 'flash:/stale-golden.bin')

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_url_boot_restores_selected_path_after_configuration_plugin_translation(self, sleep):
        self.device.platform = 'cat9k'
        self.device.model = 'c9200'
        selected = '/short/primary/image.bin'
        translated_again = '/short/secondary/image.bin'
        command = f'tftp://192.0.2.10/{selected}'
        self.device.api.get_tftp_boot_command.side_effect = lambda info: (command, selected)
        self.device.api.configure_rommon_tftp.side_effect = lambda **kwargs: configure_rommon_tftp(
            self.device, image_path=translated_again)
        conn = self.device.default
        conn.spawn.settings.MAX_BOOT_ATTEMPTS = 3
        targets = []

        def go_to(*args, **kwargs):
            targets.append((kwargs['context']['image_to_boot'], self.variables['TFTP_FILE']))
            action = next(stmt.action for stmt in kwargs['dialog']
                          if getattr(stmt.action, '__name__', '') == '_rommon_switch_boot')
            conn.spawn.sendline.side_effect = lambda cmd: targets.append((cmd.removeprefix('boot '),
                                                                         self.variables['TFTP_FILE']))
            session = {}
            for _ in range(2):
                self.variables['TFTP_FILE'] = 'flash:/stale-golden.bin'
                action(conn.spawn, session, kwargs['context'])
            self.device.state_machine.current_state = 'disable'

        conn.state_machine.go_to.side_effect = go_to
        device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()}, timeout=1)
        self.assertEqual(targets, [(command, selected)] * 3)
        self.assertEqual(conn.execute.call_args_list, [call(f'TFTP_FILE={selected}', timeout=1), call('set')] * 2)
        self.device.api.configure_rommon_tftp.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_worker_failure_is_not_reported_as_success_after_state_change(self, sleep):
        def go_to(*args, **kwargs):
            self.device.state_machine.current_state = 'disable'
            raise RuntimeError('boot transition failed after leaving ROMMON')

        self.device.default.state_machine.go_to.side_effect = go_to
        with self.assertRaisesRegex(FailedToBootException, 'boot transition failed'):
            device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()}, timeout=1)
        self.device.enable.assert_not_called()
        self.device.connection_provider.init_connection.assert_not_called()
        self.assertEqual(self.device.default.context['image_to_boot'], 'flash:/stale-golden.bin')

    def test_direct_sdk_tftp_without_image_does_not_boot_default_golden(self):
        self.device.clean = {'device_recovery': {'golden_image': ['flash:/stale-golden.bin']}}
        with self.assertRaisesRegex(SchemaError, 'missing|empty'):
            device_rommon_boot(self.device, tftp_boot={'tftp_server': '192.0.2.10'})
        self.device.api.execute_set_config_register.assert_not_called()
        self.device.default.state_machine.go_to.assert_not_called()

    def test_local_golden_list_keeps_existing_behavior(self):
        self.device.api.device_rommon_boot = Mock()
        images = ['flash:/primary.bin', 'flash:/backup.bin']
        RommonBoot().rommon_boot(Steps(), self.device, image=images)
        self.assertEqual(self.device.api.device_rommon_boot.call_args.kwargs['golden_image'], images)
        self.device.api.get_tftp_boot_command.assert_not_called()
        self.device.execute.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_explicit_local_stage_image_preserves_unused_tftp_precedence(self, sleep):
        images = ['flash:/primary.bin', 'flash:/backup.bin']
        commands = []

        def go_to(state, spawn, timeout, context, dialog):
            commands.append(context['image_to_boot'])
            self.device.state_machine.current_state = 'disable'

        self.device.default.state_machine.go_to.side_effect = go_to
        for unused in ([], [self.IMAGE, '/auto/unused.bin']):
            with self.subTest(unused=unused):
                self.device.state_machine.current_state = 'rommon'
                RommonBoot().rommon_boot(Steps(), self.device, image=images, tftp={'image': unused})
                # The existing SDK selects the first ordered local golden path;
                # the stage must preserve the entire list passed to that SDK.
                self.assertEqual(commands[-1], images[0])
                self.assertEqual(self.device.api.device_rommon_boot.call_args.kwargs['golden_image'], images)
                self.device.api.configure_rommon_tftp.assert_not_called()
                self.device.api.get_tftp_boot_command.assert_not_called()
                self.device.execute.assert_not_called()
        self.assertEqual(images, ['flash:/primary.bin', 'flash:/backup.bin'])

    def test_c9200_stage_still_rejects_active_tftp_with_explicit_local_image(self):
        self.device.api.get_recovery_details.side_effect = partial(get_c9200_recovery_details, self.device)
        steps = Steps()
        with self.assertRaises(TerminateStepSignal):
            RommonBoot().rommon_boot(steps, self.device,
                                     image=['flash:/primary.bin', 'flash:/backup.bin'],
                                     tftp={'image': [self.IMAGE, '/auto/other.bin']})
        self.assertIn('exactly one image path', steps.details[0].result.reason)
        self.device.execute.assert_not_called()
        self.device.default.state_machine.go_to.assert_not_called()

    def test_ambiguous_stage_network_list_still_fails_before_boot(self):
        for images in ([self.IMAGE, '/auto/backup.bin'], ['tftp:/primary.bin', 'tftp:/backup.bin']):
            with self.subTest(images=images), self.assertRaises(TerminateStepSignal):
                RommonBoot().rommon_boot(Steps(), self.device, image=images)
        self.device.api.device_rommon_boot.assert_not_called()

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.ThreadPoolExecutor')
    def test_incomplete_boot_future_is_not_reported_as_success(self, executor, sleep):
        def submit(*args, **kwargs):
            self.device.state_machine.current_state = 'disable'
            return Future()

        executor.return_value.submit.side_effect = submit
        with self.assertRaises(FailedToBootException):
            device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()}, timeout=0)
        self.device.enable.assert_not_called()
        executor.return_value.shutdown.assert_called_once_with(wait=True)

    @patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep')
    def test_timed_out_boot_worker_finishes_before_an_outer_retry_can_start(self, sleep):
        finished = Event()

        def go_to(*args, **kwargs):
            # Keep the real executor task alive beyond the caller's wait timeout.
            Event().wait(0.05)
            finished.set()

        self.device.default.state_machine.go_to.side_effect = go_to
        with self.assertRaises(FailedToBootException):
            device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()}, timeout=0)
        self.assertTrue(finished.is_set())
        self.assertEqual(self.device.default.context['image_to_boot'], 'flash:/stale-golden.bin')
        self.device.enable.assert_not_called()

    def test_unicon_inner_retry_executes_set_before_boot_and_handles_rejection(self):
        from unicon import Connection
        from unicon.mock.mock_device import MockDeviceTcpWrapper

        # Exercise the real Unicon dialog/execute integration, not a go_to mock.
        # The fake ROMMON reaches IOS only after the retry's TFTP_FILE assignment.
        self.device.platform = 'cat9k'
        self.device.model = 'c9300'
        for rejection in (None, 'usage', 'silent'):
            with self.subTest(rejection=rejection):
                self.device.enable.reset_mock()
                commands = {
                    'IP_ADDRESS=192.0.2.2': '', 'IP_SUBNET_MASK=255.255.255.0': '',
                    'DEFAULT_GATEWAY=192.0.2.1': '', 'TFTP_SERVER=192.0.2.10': '',
                    f'TFTP_FILE={self.IMAGE}': '',
                    'set': f'TFTP_FILE={self.IMAGE}\n',
                }
                retry_set = ('Usage: set <variable-name> <value>\n' if rejection == 'usage'
                             else '' if rejection == 'silent' else {'new_state': 'ready'})
                data = {
                    'initial': {'prompt': 'switch:', 'commands': {
                        **commands, 'boot tftp:': {'response': 'Download failed; variables reset\n',
                                                   'new_state': 'retry'}}},
                    'retry': {'prompt': 'switch:', 'commands': {
                        f'TFTP_FILE={self.IMAGE}': retry_set, 'set': 'TFTP_FILE=flash:/stale-golden.bin\n'}},
                    'ready': {'prompt': 'switch:', 'commands': {
                        'set': f'TFTP_FILE={self.IMAGE}\n',
                        'boot tftp:': {'response': f'Downloading {self.IMAGE}\n', 'new_state': 'ios'}}},
                    'ios': {'prompt': 'uut>', 'commands': {}},
                }
                server = MockDeviceTcpWrapper(device_os='iosxe', hostname='uut', state='initial',
                                              mock_data=data, port=0)
                conn = None
                try:
                    server.start()
                    conn = Connection(hostname='uut', os='iosxe', platform='cat9k', mit=True,
                                      start=[f'telnet 127.0.0.1 {server.ports[0]}'], connection_timeout=5)
                    conn.connect()
                    conn.execute = Mock(wraps=conn.execute)
                    self.device.default = conn
                    self.device.state_machine = conn.state_machine
                    self.device.execute.side_effect = conn.execute
                    if rejection:
                        self.device.api.device_rommon_boot.reset_mock()
                        steps = Steps()
                        with patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep'), \
                                self.assertRaises(TerminateStepSignal):
                            RommonBoot().rommon_boot(
                                steps, self.device, tftp={'image': self.nested_metadata()}, timeout=5)
                        if rejection == 'usage':
                            self.assertIn('Usage: set', steps.details[0].result.reason)
                        else:
                            self.assertIn('readback did not match', steps.details[0].result.reason)
                        self.device.api.device_rommon_boot.assert_called_once()
                        self.device.enable.assert_not_called()
                        self.assertEqual(conn.state_machine.current_state, 'rommon')
                    else:
                        with patch('genie.libs.sdk.apis.iosxe.rommon.utils.time.sleep'):
                            device_rommon_boot(self.device, tftp_boot={'image': self.nested_metadata()}, timeout=5)
                        self.assertEqual(conn.state_machine.current_state, 'disable')
                        self.device.enable.assert_called_once()
                    file_commands = [args[0] for args, _ in conn.execute.call_args_list
                                     if args[0].startswith('TFTP_FILE=')]
                    self.assertEqual(file_commands, [f'TFTP_FILE={self.IMAGE}'] * 2)
                finally:
                    if conn is not None:
                        conn.disconnect()
                    server.stop()
