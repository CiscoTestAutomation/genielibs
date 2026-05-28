import sys
import unittest
import yaml
from unittest.mock import Mock

from pyats.aetest.script import TestScript
from genie.libs.health.health import Health, SECTION_CLASS_MAPPING
from genie.libs.health import health_yamls

from pyats.easypy import runtime
from pyats.aetest.tests.scripts import testScript


class TestHealth(unittest.TestCase):

    def test__select_health(self):
        self.maxDiff = None
        hlth = Health()
        section = Mock()
        data = {
            'execute': {
                'device': 'uut',
                'command': 'show running-config',
                'health_sections': []
            }
        }

        search_keywords = ['.*']
        arg_name = 'health_tc_sections'

        for section_type in [
                'CommonSetup', 'CommonCleanup', 'SetupSection',
                'CleanupSection', 'TestSection', 'TestCase'
        ]:
            test_data = data.copy()
            test_data['execute']['health_sections'] = [
                'type:{}'.format(section_type)
            ]
            section = SECTION_CLASS_MAPPING.get(section_type)
            section.uid = 'TestHealth'
            section.parent = testScript
            runtime.args.health_tc_sections = ''
            selected = hlth._select_health(section, test_data, search_keywords,
                                           arg_name)
            self.assertEqual(selected, [{
                'execute': {
                     'device': 'uut',
                     'command': 'show running-config',
                     'health_sections': ['type:{}'.format(section_type)]
                 }
            }])

    def test__select_health_negative(self):
        self.maxDiff = None
        hlth = Health()
        section = Mock()
        data = {
            'execute': {
                'device': 'uut',
                'command': 'show running-config',
            }
        }

        search_keywords = ['.*']
        arg_name = 'health_tc_sections'

        for section_type in [
                'CommonSetup', 'CommonCleanup', 'SetupSection',
                'CleanupSection', 'TestSection', 'TestCase'
        ]:
            test_data = data.copy()
            section = SECTION_CLASS_MAPPING.get(section_type)
            section.uid = 'TestHealth'
            section.parent = testScript
            runtime.args.health_tc_sections = ''
            selected = hlth._select_health(section, test_data, search_keywords,
                                           arg_name)
            self.assertEqual(selected, [{
                'execute': {
                     'device': 'uut',
                     'command': 'show running-config'
                 }
            }])


def _load_pyats_health_yaml():
    """Load and return the parsed pyats_health.yaml as a dict."""
    with open(health_yamls.pyats_health_yaml) as f:
        return yaml.safe_load(f)


def _get_section_actions(health_yaml, section_name):
    """Return the list of action dicts for a named test_section entry."""
    processors = health_yaml.get('pyats_health_processors', health_yaml)
    for section in processors.get('test_sections', []):
        if section_name in section:
            return section[section_name]
    return []


def _collect_api_actions(actions):
    """Recursively collect all 'api' action dicts from a nested action list."""
    found = []
    for item in actions or []:
        if isinstance(item, dict):
            if 'api' in item:
                found.append(item['api'])
            # run_condition wraps actions
            for key in ('run_condition', 'loop'):
                if key in item:
                    sub = item[key]
                    found.extend(_collect_api_actions(sub.get('actions', [])))
    return found


class TestCrashinfoYamlWiring(unittest.TestCase):
    """Verify the crashinfo and crashinfo_pre_check sections in pyats_health.yaml."""

    @classmethod
    def setUpClass(cls):
        cls.health_yaml = _load_pyats_health_yaml()

    def test_crashinfo_wiring(self):
        """crashinfo: exists, targets type:TestCase, processor=post, calls health_crashinfo."""
        actions = _get_section_actions(self.health_yaml, 'crashinfo')
        self.assertTrue(actions, "crashinfo section missing from pyats_health.yaml")
        api_actions = _collect_api_actions(actions)
        self.assertTrue(api_actions, "No api actions found in crashinfo section")
        for api in api_actions:
            self.assertIn('type:TestCase', api.get('health_tc_sections', []))
            self.assertEqual(api.get('processor'), 'post')
            self.assertEqual(api.get('function'), 'health_crashinfo')

    def test_crashinfo_pre_check_wiring(self):
        """crashinfo_pre_check: exists, targets type:CommonSetup, processor=post,
        failed_result_status=passx, calls health_crashinfo."""
        actions = _get_section_actions(self.health_yaml, 'crashinfo_pre_check')
        self.assertTrue(actions, "crashinfo_pre_check section missing from pyats_health.yaml")
        api_actions = _collect_api_actions(actions)
        self.assertTrue(api_actions, "No api actions found in crashinfo_pre_check section")
        for api in api_actions:
            self.assertIn('type:CommonSetup', api.get('health_tc_sections', []))
            self.assertEqual(api.get('processor'), 'post')
            self.assertEqual(api.get('failed_result_status'), 'passx')
            self.assertEqual(api.get('function'), 'health_crashinfo')

    def test_crashinfo_pre_check_no_save_negative(self):
        """crashinfo_pre_check must NOT have a save: block — pre-existing filenames
        must not pollute health_value in reports."""
        api_actions = _collect_api_actions(
            _get_section_actions(self.health_yaml, 'crashinfo_pre_check'))
        for api in api_actions:
            self.assertNotIn('save', api, "crashinfo_pre_check must not have a 'save:' block")

