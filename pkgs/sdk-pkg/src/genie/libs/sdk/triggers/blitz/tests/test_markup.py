#! /usr/bin/env python
import os
import yaml
import unittest
import tempfile

from unittest import mock
from unittest.mock import patch, mock_open

from genie.utils.dq import Dq
from genie.testbed import load
from genie.libs.sdk.triggers.blitz.blitz import Blitz
from genie.libs.sdk.triggers.blitz.markup import (apply_dictionary_filter,
                                                  apply_regex_findall,
                                                  apply_regex_filter,
                                                  get_variable,
                                                  save_output_to_file,
                                                  save_variable,
                                                  apply_list_filter,
                                                  _load_saved_variable)


from pyats.easypy import Task
from pyats.easypy.job import Job
from pyats.easypy import runtime
from pyats.aetest.parameters import ParameterMap
from pyats.easypy.common_funcs import init_runtime
from pyats.results import Passed, Failed, Errored, Skipped,\
                          Aborted, Passx, Blocked


class TestMarkup(unittest.TestCase):

    dict_output = {'platform': {'name': 'Nexus',
                   'os': 'NX-OS',
                   'software': {'bios_version': '07.33',
                    'system_version': '9.3(3) [build 9.3(3)IDI9(0.509)]',
                    'bios_compile_time': '08/04/2015',
                    'system_image_file': 'bootflash:///system-image-N93_3-00613722415136',
                    'system_compile_time': '10/22/2019 10:00:00 [10/22/2019 16:57:31]'},
                   'hardware': {'model': 'Nexus9000 C9396PX',
                    'chassis': 'Nexus9000 C9396PX',
                    'slots': 'None',
                    'rp': 'None',
                    'cpu': 'Intel(R) Core(TM) i3- CPU @ 2.50GHz',
                    'memory': '16399900 kB',
                    'processor_board_id': 'SAL1914CNL6',
                    'device_name': 'N93_3',
                    'bootflash': '51496280 kB'},
                   'kernel_uptime': {'days': 61, 'hours': 22, 'minutes': 8, 'seconds': 40},
                   'reason': 'Reset Requested by CLI command reload',
                   'system_version': '9.3(3)'}}

    str_output = """

        2020-11-24 12:25:43,769: %UNICON-INFO: +++ N93_3: executing command 'show version' +++
        show version
        Cisco Nexus Operating System (NX-OS) Software
        TAC support: http://www.cisco.com/tac
        Copyright (C) 2002-2019, Cisco and/or its affiliates.
        All rights reserved.
        The copyrights to certain works contained in this software are
        owned by other third parties and used and distributed under their own
        licenses, such as open source.  This software is provided "as is," and unless
        otherwise stated, there is no warranty, express or implied, including but not
        limited to warranties of merchantability and fitness for a particular purpose.
        Certain components of this software are licensed under
        the GNU General Public License (GPL) version 2.0 or
        GNU General Public License (GPL) version 3.0  or the GNU
        Lesser General Public License (LGPL) Version 2.1 or
        Lesser General Public License (LGPL) Version 2.0.
        A copy of each such license is available at
        http://www.opensource.org/licenses/gpl-2.0.php and
        http://opensource.org/licenses/gpl-3.0.html and
        http://www.opensource.org/licenses/lgpl-2.1.php and
        http://www.gnu.org/licenses/old-licenses/library.txt.

        Software
          BIOS: version 07.33
         NXOS: version 9.3(3) [build 9.3(3)IDI9(0.509)]
          BIOS compile time:  08/04/2015
          NXOS image file is: bootflash:///system-image-N93_3-00613722415136
          NXOS compile time:  10/22/2019 10:00:00 [10/22/2019 16:57:31]


        Hardware
          cisco Nexus9000 C9396PX Chassis
          Intel(R) Core(TM) i3- CPU @ 2.50GHz with 16399900 kB of memory.
          Processor Board ID SAL1914CNL6

          Device name: N93_3
          bootflash:   51496280 kB
        Kernel uptime is 61 day(s), 22 hour(s), 33 minute(s), 56 second(s)

        Last reset at 930930 usecs after Wed Sep 23 13:59:45 2020
          Reason: Reset Requested by CLI command reload
          System version: 9.3(3)
          Service:

        plugin
          Core Plugin, Ethernet Plugin

        Active Package(s):
    """

    def setUp(self):

        dir_name = os.path.dirname(os.path.abspath(__file__))
        mfc = MockFuncClass()
        self.testbed = load(os.path.join(dir_name, 'mock_testbeds/testbed.yaml'))
        Blitz.parameters = ParameterMap()
        Blitz.uid = 'test.dev'
        Blitz.parameters['testbed'] = self.testbed
        Blitz.parameters['save_variable_name'] = {'dev_name': 'PE2',
                                                  'command':'sh version',
                                                  'sub_command': 'interface',
                                                  'type_k': 1500,
                                                  'list_item': [177,24,13,45],
                                                  'iter_class': mfc,
                                                  'dict1': {'st': "name"}}

        self.blitz_obj = Blitz()
        self.uid = self.blitz_obj.uid
        self.blitz_obj.parent = self
        self.blitz_obj.parent.parameters = mock.Mock()
        self.blitz_obj.parameters['test_sections'] = [{'section1': [{'execute': {'command': 'cmd', 'device': 'PE1'}}]}]
        sections = self.blitz_obj._discover()
        self.section = sections[0].__testcls__(sections[0])

    def test_dq_filter_list_index(self):

        list_output = [1,2,3,4,6,7,8,9999,854]
        list_index = 3
        filtered_out = apply_list_filter(self.blitz_obj,
                                         list_output,
                                         list_index=list_index)

        self.assertEqual(filtered_out, 4)

    def test_dq_filter_list_slice(self):

        list_output = [1,2,3,4,6,7,8,9999,854]
        list_index = "[1:4]"
        filtered_out = apply_list_filter(self.blitz_obj,
                                         list_output,
                                         list_index=list_index)

        self.assertEqual(filtered_out, [2,3,4])

    def test_dq_filter_list_regex(self):

        list_output = ["aba", "yes"]
        filtered_out = apply_list_filter(self.blitz_obj,
                                         list_output,
                                         filters='yes')
        self.assertEqual(filtered_out, ["yes"])

        filtered_out = apply_list_filter(self.blitz_obj,
                                         list_output,
                                         filters=r'\d')
        self.assertEqual(filtered_out, [])

    def test_dq_filter(self):

        filters = "contains('software')"
        filtered_out = apply_dictionary_filter(self.blitz_obj, self.dict_output, filters)

        self.assertEqual(filtered_out, {'platform': {'software': {'bios_version': '07.33',
                                        'system_version': '9.3(3) [build 9.3(3)IDI9(0.509)]',
                                        'bios_compile_time': '08/04/2015',
                                        'system_image_file': 'bootflash:///system-image-N93_3-00613722415136',
                                        'system_compile_time': '10/22/2019 10:00:00 [10/22/2019 16:57:31]'}}})
    def test_string_filter(self):

        filters = r"Device\s+name:\s+(?P<dev>.*)"
        filtered_out = apply_regex_filter(self.blitz_obj, self.str_output, filters)
        self.assertEqual(filtered_out, {'dev': 'N93_3'})

        filters = r"Device\s+name:\s+(?P<dev>NO MATCH)"
        filtered_out = apply_regex_filter(self.blitz_obj, self.str_output, filters)
        self.assertEqual(filtered_out, {'dev': ''})

    def test_no_filter(self):
        # with No filter
        filtered_out = apply_dictionary_filter(self.blitz_obj, output=self.dict_output)
        self.assertEqual(filtered_out, self.dict_output)
        filtered_out = apply_regex_filter(self.blitz_obj, output=self.str_output)
        self.assertEqual(filtered_out, self.str_output)

    def test_string_findall_match(self):
        pattern = r"(\d{2}\/\d{2}\/\d{4})"
        matches = apply_regex_findall(self, output=self.str_output, pattern=pattern)
        self.assertEqual(matches, ['08/04/2015', '10/22/2019', '10/22/2019'])

    def test_string_findall_no_match(self):
        pattern = r"(\d{2}-\d{2}-\d{4})"
        matches = apply_regex_findall(self, output=self.str_output, pattern=pattern)
        self.assertEqual(matches, [])

    def test_get_variable_replace(self):

        kwargs = {'command': r"%VARIABLES{command}",
                  'device': 'PE2',
                  'self': self.blitz_obj,
                  'section': self.section}

        replaced_kwargs = get_variable(**kwargs)
        # check if replacement is done
        self.assertEqual(replaced_kwargs['command'], self.blitz_obj.parameters['save_variable_name']['command'])

    def test_get_variable_replace_replace_keep_type(self):

        kwargs = {'self': self.blitz_obj,
                  'item': {'value': r"%VARIABLES{type_k}",
                           'val': 11,
                           'ls': ['a', {'b':1}]},
                  'section': self.section}

        replaced_kwargs = get_variable(**kwargs)
        # check if type would stay the same
        self.assertEqual(type(replaced_kwargs['item']['value']), int)

    def test_get_variable_replace_replace_mid_str(self):

        kwargs = {'cmd': r"show  %VARIABLES{sub_command}",
                  'self': self.blitz_obj,
                  'section': self.section}

        replaced_kwargs = get_variable(**kwargs)
        self.assertEqual(replaced_kwargs['cmd'], 'show  interface')

    def test_get_variable_replace_replace_list_item(self):

        kwargs = {'cmd': r"%VARIABLES{list_item[2]}",
                  'self': self.blitz_obj,
                  'section': self.section}
        replaced_kwargs = get_variable(**kwargs)
        self.assertEqual(replaced_kwargs['cmd'], 13)

    # TODO check why ._keys and ._values doesnt work
    def test_get_variable_replace_dict_item(self):
        pass

    def test_get_variable_replace_replace_iter_fucnt(self):

        kwargs = {'a': r"%VARIABLES{iter_class.mock_func}",
                  'self': self.blitz_obj,
                  'section': self.section}
        replaced_kwargs = get_variable(**kwargs)
        self.assertEqual(replaced_kwargs['a'], 'mock func returned val')

    def test_save_and_load_variable(self):

        saved_variable = 'var1'
        saved_value = 'aa'
        save_variable(self.blitz_obj, self.section, saved_variable, saved_value)
        self.assertEqual(
            self.blitz_obj.parameters['save_variable_name'][saved_variable], saved_value)

        _, val = _load_saved_variable(self.blitz_obj, self.section, val=saved_value, key=saved_variable)
        self.assertEqual(val, saved_value)

    def test_save_and_load_variable_empty(self):

        saved_variable = 'var2'
        saved_value = ''
        save_variable(self.blitz_obj, self.section, saved_variable, saved_value)
        self.assertEqual(
            self.blitz_obj.parameters['save_variable_name'][saved_variable], saved_value)

        _, val = _load_saved_variable(self.blitz_obj, self.section, val=saved_value, key=saved_variable)
        self.assertEqual(val, saved_value)

    def test_save_variable_append(self):

        save_variable(self.blitz_obj, self.section, 'sub_command', 'vrf', append=True)
        self.assertEqual(
            self.blitz_obj.parameters['save_variable_name']['sub_command'], 'interface\nvrf')

    def test_save_variable_append_in_empty_list(self):

        save_variable(self.blitz_obj, self.section, 'new_item', 'VRF1', append_in_list=True)
        self.assertEqual(
            self.blitz_obj.parameters['save_variable_name']['new_item'], ['VRF1'])

    def test_save_variable_append_in_existing_list(self):

        save_variable(self.blitz_obj, self.section, 'list_item', 9000, append_in_list=True)
        self.assertEqual(
            self.blitz_obj.parameters['save_variable_name']['list_item'], [177,24,13,45, 9000])

    @patch('builtins.open', new_callable=mock_open())
    def test_save_output_write_to_file(self, mock_open_file):
        test_content = ['CSR1000V']
        file_name = 'filename.txt'

        save_output_to_file(file_name, test_content)

        file_path = os.path.join(runtime.directory, file_name)

        mock_open_file.assert_called_once_with(file_path, "w")
        mock_open_file.return_value.__enter__().\
            write.assert_called_once_with("['CSR1000V']\n")

    @patch('builtins.open', new_callable=mock_open(read_data='test1\n'))
    def test_save_output_append_to_file(self, mock_open_file):
        test_content = ['CSR1000V']
        file_name = 'filename.txt'

        save_output_to_file(file_name, test_content, append_to_file='True')

        file_path = os.path.join(runtime.directory, file_name)

        mock_open_file.assert_called_once_with(file_path, "a")
        mock_open_file.return_value.__enter__().\
            write.assert_called_once_with("['CSR1000V']\n")


class MockFuncClass(object):

    @property
    def mock_func(self):
        return 'mock func returned val'

if __name__ == '__main__':
    unittest.main()
