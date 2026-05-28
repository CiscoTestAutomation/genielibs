import argparse
import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from genie.libs.sdk.triggers.blitz.maple_converter import plugin as plugin_module
from genie.libs.sdk.triggers.blitz.maple_converter import testsuite_converter as ts_module
from genie.libs.sdk.triggers.blitz.maple_converter.plugin import MapleCleanPlugin
from genie.libs.sdk.triggers.blitz.maple_converter.testsuite_converter import (
    Testsuite_Converter as MapleTestsuiteConverter,
)


class Args(SimpleNamespace):
    def __contains__(self, name):
        return hasattr(self, name)


class FakeCleaner(object):
    pass


class RuntimeObject(object):
    pass


class TestMapleCleanPluginAdditional(unittest.TestCase):

    def make_plugin(self, runtime):
        plugin = object.__new__(MapleCleanPlugin)
        plugin.runtime = runtime
        plugin.logfile = None
        return plugin

    def test_configure_parser_legacy_and_non_legacy(self):
        parser = MapleCleanPlugin.configure_parser(
            argparse.ArgumentParser(), legacy_cli=True)
        args = parser.parse_args(['-maple_testsuite', 'suite.yaml'])
        self.assertEqual(args.testsuite_file, 'suite.yaml')

        parser = MapleCleanPlugin.configure_parser(
            argparse.ArgumentParser(), legacy_cli=False)
        args = parser.parse_args(['--maple-testsuite', 'suite.yaml'])
        self.assertEqual(args.testsuite_file, 'suite.yaml')

    def test_update_tims_folder_id_success_and_missing_device(self):
        version = Mock()
        version.q.contains.return_value.get_values.return_value = (
            'bootflash:///image.bin'
        )
        device = Mock()
        device.name = 'tims'
        device.parse.return_value = version

        runtime = RuntimeObject()
        runtime.testbed = SimpleNamespace(
            testbed=SimpleNamespace(custom={'tims_device': 'tims'}),
            devices={'tims': device},
        )
        task = SimpleNamespace(kwargs={'tims_folder': 'folder'})

        self.make_plugin(runtime).update_tims_folder_id(task)

        device.connect.assert_called_once()
        device.parse.assert_called_once_with('show version')
        device.disconnect.assert_called_once()
        self.assertEqual(task.kwargs['tims_folder'], 'folder/image.bin')

        runtime.testbed.testbed.custom['tims_device'] = 'missing'
        task = SimpleNamespace(kwargs={'tims_folder': 'folder'})
        self.make_plugin(runtime).update_tims_folder_id(task)
        self.assertEqual(task.kwargs['tims_folder'], 'folder')

    def test_pre_task_early_returns_and_clean_file_errors(self):
        args = Args(testsuite_file=None, clean_files=None)
        runtime = RuntimeObject()
        runtime.args = args
        runtime.directory = '.'
        runtime.testbed = Mock()
        task = SimpleNamespace(kwargs={})
        plugin = self.make_plugin(runtime)

        with patch.object(plugin_module.runtime, 'args', args, create=True):
            self.assertIsNone(plugin.pre_task(task, Mock()))

        args = Args(testsuite_file='suite.yaml', clean_files=None)
        runtime.args = args
        with patch.object(plugin_module.runtime, 'args', args, create=True):
            self.assertIsNone(plugin.pre_task(task, Mock()))

        with tempfile.TemporaryDirectory() as tmpdir:
            missing = os.path.join(tmpdir, 'missing.yaml')
            args = Args(testsuite_file='suite.yaml', clean_files=[missing])
            runtime = RuntimeObject()
            runtime.args = args
            runtime.directory = tmpdir
            runtime.testbed = Mock()
            plugin = self.make_plugin(runtime)
            with patch.object(plugin_module.runtime, 'args', args, create=True), \
                    patch.object(plugin_module, 'KleenexPlugin',
                                 return_value=Mock()):
                with self.assertRaises(FileNotFoundError):
                    plugin.pre_task(task, Mock())

            clean_file = os.path.join(tmpdir, 'clean.yaml')
            with open(clean_file, 'w') as clean_file_obj:
                clean_file_obj.write('cleaners: {}')
            args.clean_files = [clean_file]
            with patch.object(plugin_module.runtime, 'args', args, create=True), \
                    patch.object(plugin_module, 'KleenexPlugin',
                                 return_value=Mock()), \
                    patch.object(plugin_module.os, 'access', return_value=False):
                with self.assertRaises(PermissionError):
                    plugin.pre_task(task, Mock())

    def test_pre_task_clean_file_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            clean_file = os.path.join(tmpdir, 'clean.yaml')
            with open(clean_file, 'w') as clean_file_obj:
                clean_file_obj.write('cleaners: {}')

            args = Args(
                testsuite_file='suite.yaml',
                clean_files=[clean_file],
                invoke_clean=True,
            )
            runtime = RuntimeObject()
            runtime.args = args
            runtime.directory = tmpdir
            runtime.testbed = Mock()
            task = SimpleNamespace(kwargs={})
            reporter = Mock()
            plugin = self.make_plugin(runtime)

            fake_kleenex = Mock()
            fake_loader = Mock()
            fake_loader.load.return_value = {
                'cleaners': {'cleaner': {'class': FakeCleaner}},
                'clean_devices': 'uut',
            }

            with patch.object(plugin_module.runtime, 'args', args, create=True), \
                    patch.object(plugin_module, 'KleenexPlugin',
                                 return_value=fake_kleenex), \
                    patch.object(plugin_module, 'KleenexFileLoader',
                                 return_value=fake_loader), \
                    patch.object(plugin_module.managed_handlers, 'tasklog',
                                 SimpleNamespace(logfile='task.log'),
                                 create=True):
                plugin.pre_task(task, reporter)

            self.assertTrue(os.path.isfile(
                os.path.join(tmpdir, 'testbed.clean.yaml')))
            self.assertTrue(os.path.isfile(
                os.path.join(tmpdir, 'testbed.clean.extended.yaml')))
            self.assertEqual(fake_kleenex.clean_devices, ['uut'])
            self.assertIsNone(fake_kleenex.logical_testbed_file)
            fake_kleenex.do_bringup_clean_logic.assert_called_once_with(
                task=task, reporter=reporter)


class TestTestsuiteConverterAdditional(unittest.TestCase):

    def test_grun_kwargs_generator_reads_tasks_and_clean_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            clean_file = os.path.join(tmpdir, 'clean.yaml')
            testsuite_file = os.path.join(tmpdir, 'suite.yaml')
            with open(clean_file, 'w') as clean_file_obj:
                clean_file_obj.write('cleaners: {}')
            with open(testsuite_file, 'w') as testsuite_file_obj:
                testsuite_file_obj.write("""
tasks:
  task-1:
    testcase_control: abort-on-failure
    teststep_control: continue-on-failure
    tims_testplan_folder: plan
    tims_result_folder: result
    testbed_file: testbed.yaml
    testcase_file: testcase.yaml
    run: tc1, tc2
    skip: tc3
    clean_file: {clean_file}
""".format(clean_file=clean_file))

            args = Args()
            converter = MapleTestsuiteConverter(testsuite_file)

            with patch.object(ts_module.runtime, 'args', args, create=True), \
                    patch.object(MapleTestsuiteConverter,
                                 'updating_grun_kwargs',
                                 return_value={'converted': True}) as update:
                kwargs = list(converter.grun_kwargs_generator())

            self.assertEqual(kwargs, [{'converted': True}])
            self.assertEqual(args.clean_files, [clean_file])
            self.assertTrue(args.invoke_clean)
            self.assertTrue(args.check_all_devices_up)
            update.assert_called_once()
            _, ts_keywords, run_testcases, skip_testcases = update.call_args[0]
            self.assertEqual(ts_keywords['testcase_file'], 'testcase.yaml')
            self.assertEqual(run_testcases, ['tc1', ' tc2'])
            self.assertEqual(skip_testcases, ['tc3'])

    def test_updating_grun_kwargs_success_and_failure(self):
        converter = MapleTestsuiteConverter('suite.yaml')
        fake_converter = Mock()
        fake_converter.convert.return_value = ['tc1', 'tc2', 'tc3']
        fake_converter.blitz_file = 'blitz.yaml'
        fake_converter.testbed_file = 'testbed.yaml'
        ts_keywords = {
            'testcase_file': 'maple.yaml',
            'testbed_file': 'testbed.yaml',
            'testcase_control': 'abort-on-failure',
            'teststep_control': 'continue-on-failure',
            'tims_testplan_folder': 'plan',
            'tims_result_folder': 'result',
        }

        with patch.object(ts_module, 'Converter',
                          return_value=fake_converter) as converter_cls, \
                patch.object(converter, '_subsection_datafile_creator',
                             return_value='subsection.yaml'), \
                patch.object(converter, '_mapping_datafile_creator',
                             return_value='mapping.yaml'):
            kwargs = converter.updating_grun_kwargs(
                {}, ts_keywords, [' tc2 '], [])

        converter_cls.assert_called_once_with(
            'maple.yaml',
            testbed='testbed.yaml',
            testcase_control='abort-on-failure',
            teststep_control='continue-on-failure',
            tims_testplan_folder='plan',
        )
        self.assertEqual(kwargs['trigger_datafile'], 'blitz.yaml')
        self.assertEqual(kwargs['testbed'], 'testbed.yaml')
        self.assertEqual(kwargs['trigger_uids'], ['tc2'])
        self.assertEqual(kwargs['tims_folder'], 'result')
        self.assertEqual(kwargs['mapping_datafile'], 'mapping.yaml')

        fake_converter.convert.side_effect = RuntimeError('bad maple')
        with patch.object(ts_module, 'Converter',
                          return_value=fake_converter):
            with self.assertRaisesRegex(Exception, 'Unable to translate'):
                converter.updating_grun_kwargs({}, ts_keywords, [], [])

    def test_datafile_creators_and_trigger_uid_filtering(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            testsuite_file = os.path.join(tmpdir, 'suite.yaml')
            with open(testsuite_file, 'w') as testsuite_file_obj:
                testsuite_file_obj.write('tasks: {}')
            converter = MapleTestsuiteConverter(testsuite_file)

            with patch.object(ts_module.ruamel.yaml, 'round_trip_dump',
                              return_value='dumped', create=True):
                subsection_file = converter._subsection_datafile_creator()
            self.assertTrue(os.path.isfile(subsection_file))
            self.assertTrue(subsection_file.endswith(
                'additional_datafiles/subsection_datafile.yaml'))

            devices = {
                'ha': SimpleNamespace(connections={'a': {}, 'b': {}}),
                'single': SimpleNamespace(connections={'a': {}}),
                'other': SimpleNamespace(
                    connections={'default': {}, 'mgmt': {}}),
            }
            fake_testbed = SimpleNamespace(devices=devices)

            with patch.object(ts_module, 'load', return_value=fake_testbed), \
                    patch.object(ts_module.ruamel.yaml, 'round_trip_dump',
                                 return_value='dumped',
                                 create=True):
                mapping_file = converter._mapping_datafile_creator(
                    'testbed.yaml')

            self.assertTrue(os.path.isfile(mapping_file))
            self.assertTrue(mapping_file.endswith(
                'additional_datafiles/mapping_datafile.yaml'))

            self.assertEqual(
                converter._update_trigger_uids(
                    ['tc1', 'tc2'], run_testcases=[' tc3 ', '']),
                ['tc3'],
            )
            self.assertEqual(
                converter._update_trigger_uids(
                    ['tc1', 'tc2'], skip_testcases=['tc2']),
                ['tc2'],
            )
            self.assertIsNone(converter._update_trigger_uids(['tc1']))


if __name__ == '__main__':
    unittest.main()
