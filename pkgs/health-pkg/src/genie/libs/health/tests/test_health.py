import sys
import unittest
from unittest.mock import Mock

from pyats.aetest.script import TestScript
from genie.libs.health.health import Health, SECTION_CLASS_MAPPING

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
