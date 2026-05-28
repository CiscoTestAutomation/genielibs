import json
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pyats.results import Failed, Passed

from genie.libs.sdk.triggers.blitz import maple as maple_module


class ActionSteps(object):

    def __init__(self):
        self.result = Passed

    def start(self, *args, **kwargs):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def failed(self, *args, **kwargs):
        self.result = Failed

    def passed(self, *args, **kwargs):
        self.result = Passed


class TestMapleAdditional(unittest.TestCase):

    def _blitz(self):
        parent = SimpleNamespace(parameters={})
        return SimpleNamespace(
            parameters={
                'testbed': SimpleNamespace(name='tb'),
                'save_variable_name': {},
            },
            parent=parent,
        )

    def _section(self, blitz):
        return SimpleNamespace(parent=blitz.parent)

    def _plugin_input(self, plugin_type, data):
        return json.dumps({
            'type': 'cli',
            'commands': '{}:{}'.format(plugin_type, json.dumps(data)),
        })

    def test_maple_calls_default_command_plugin_and_saves_outputs(self):
        seen_objects = {}

        def process(objects):
            seen_objects.update(objects)
            return {
                'result': [True],
                'output': 'plugin-output',
                'matchObjs': {'match_value': 'saved'},
                'ixiaObjs': {'ixia_value': 'saved', 'empty_value': {}},
            }

        plugin_source = SimpleNamespace(
            __name__='plugins.system.Commands',
            __package__='plugins.system',
            process=process,
        )
        blitz = self._blitz()
        device = SimpleNamespace(name='PE1', type='router')

        with patch.object(maple_module.importlib, 'import_module',
                          return_value=plugin_source):
            output = maple_module.maple(
                self=blitz,
                steps=ActionSteps(),
                device=device,
                maple_plugin_input=self._plugin_input(
                    'command',
                    {
                        'method': 'process',
                        'options': [{'duration': '1'}],
                    },
                ),
                maple_action='apply',
                section=self._section(blitz),
            )

        self.assertEqual(output, 'plugin-output')
        self.assertEqual(seen_objects['duration'], '1')
        self.assertEqual(seen_objects['type'], 'apply')
        self.assertEqual(
            blitz.parameters['save_variable_name']['match_value'],
            'saved',
        )
        self.assertEqual(
            blitz.parameters['save_variable_name']['ixia_value'],
            'saved',
        )
        self.assertNotIn('empty_value', blitz.parameters['save_variable_name'])

    def test_maple_calls_class_plugin_with_confirm_result(self):
        class PluginClass(object):

            def confirm(self, objects):
                return {'result': True, 'output': objects['output']}

        plugin_module = SimpleNamespace(PluginClass=PluginClass)
        blitz = self._blitz()
        device = SimpleNamespace(name='PE1', type='router')

        with patch.object(maple_module.importlib, 'import_module',
                          return_value=plugin_module):
            output = maple_module.maple(
                self=blitz,
                steps=ActionSteps(),
                device=device,
                maple_plugin_input=self._plugin_input(
                    'confirm',
                    {
                        'package': 'custom.plugins',
                        'class': 'PluginClass',
                        'method': 'confirm',
                    },
                ),
                output='show-output',
                section=self._section(blitz),
            )

        self.assertEqual(output, 'show-output')

    def test_maple_matcher_plugin_executes_device_command(self):
        def matcher(objects):
            return {'output': objects['output']}

        plugin_source = SimpleNamespace(
            __name__='plugins.system.Commands',
            __package__='plugins.system',
            matcher=matcher,
        )
        blitz = self._blitz()
        device = SimpleNamespace(
            name='PE1',
            type='router',
            execute=Mock(return_value='command-output'),
        )

        with patch.object(maple_module.importlib, 'import_module',
                          return_value=plugin_source):
            output = maple_module.maple(
                self=blitz,
                steps=ActionSteps(),
                device=device,
                maple_plugin_input=self._plugin_input(
                    'matcher',
                    {
                        'method': 'matcher',
                        'command': 'show version',
                    },
                ),
                section=self._section(blitz),
            )

        self.assertEqual(output, 'command-output')
        device.execute.assert_called_once_with('show version')

    def test_maple_plugin_input_adds_ixia_saved_objects(self):
        plugin_source = SimpleNamespace(
            __name__='plugins.system.Commands',
            __package__='plugins.system',
            process=lambda objects: {'output': objects},
        )
        blitz = self._blitz()
        blitz.parameters['save_variable_name'].update({
            'ixiaNet': {'net': 'value'},
            'ixiaNetSelf': {'self': 'value'},
            'ixiaNetStop': {'stop': 'value'},
        })
        device = SimpleNamespace(name='IXIA', type='ixia')

        with patch.object(maple_module.importlib, 'import_module',
                          return_value=plugin_source):
            objects, source = maple_module._maple_plugins_input(
                self=blitz,
                steps=ActionSteps(),
                device=device,
                plugin_data={},
                maple_action=None,
                matched_group={'plugin_type': 'command'},
                maple_plugin_input={'commands': 'command:{}'},
                package=None,
                method='process',
            )

        self.assertIs(source, plugin_source)
        self.assertEqual(objects['ixiaObjs']['ixiaNet'], {'net': 'value'})
        self.assertEqual(objects['ixiaObjs']['ixiaNetSelf'], {'self': 'value'})
        self.assertEqual(objects['ixiaObjs']['ixiaNetStop'], {'stop': 'value'})

    def test_maple_rejects_missing_method(self):
        with self.assertRaises(Exception):
            maple_module.maple(
                self=self._blitz(),
                steps=ActionSteps(),
                device=SimpleNamespace(name='PE1', type='router'),
                maple_plugin_input=self._plugin_input('command', {}),
                section=SimpleNamespace(),
            )

    def test_maple_search_include_not_found_marks_failed(self):
        steps = ActionSteps()

        maple_module.maple_search(
            self=self._blitz(),
            steps=steps,
            search_string='line one\nline two',
            device=SimpleNamespace(name='PE1'),
            include=['missing'],
        )

        self.assertEqual(steps.result, Failed)
